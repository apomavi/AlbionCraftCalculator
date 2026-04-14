from __future__ import annotations

import os
import time
from typing import Any

from crewai import LLM
from crewai.llms.base_llm import BaseLLM
from pydantic import PrivateAttr

from albion_factory.fallback_logger import log_fallback_event


DEFAULT_MODELS = {
    "report_lead": "ollama/qwen2.5-coder:14b",
    "report_researcher": "gemini/gemini-2.5-flash-lite",
    "report_validator": "ollama/qwen2.5-coder:14b",
    "factory_lead_manager": "ollama/qwen2.5-coder:14b",
    "factory_researcher": "gemini/gemini-2.5-flash-lite",
    "factory_coder": "ollama/qwen2.5-coder:14b",
    "factory_tester": "ollama/qwen2.5-coder:14b",
    "factory_validator": "ollama/qwen2.5-coder:14b",
    "ops_lead_manager": "ollama/qwen2.5-coder:14b",
    "ops_researcher": "gemini/gemini-2.5-flash-lite",
    "ops_data_collector": "ollama/qwen2.5-coder:14b",
    "ops_tester": "ollama/qwen2.5-coder:14b",
    "ops_validator": "ollama/qwen2.5-coder:14b",
}


def _clean_model_name(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def _dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def resolve_model(role_key: str, default: str | None = None) -> str:
    role_env_key = f"MODEL_{role_key.upper()}"
    role_override = _clean_model_name(os.getenv(role_env_key))
    if role_override:
        return role_override

    global_default = _clean_model_name(os.getenv("MODEL_DEFAULT"))
    if global_default:
        return global_default

    yaml_default = _clean_model_name(default)
    if yaml_default:
        return yaml_default

    return DEFAULT_MODELS[role_key]


def resolve_model_chain(role_key: str, default: str | None = None) -> list[str]:
    chain_env_key = f"MODEL_CHAIN_{role_key.upper()}"
    chain_env = _clean_model_name(os.getenv(chain_env_key))
    if chain_env:
        return _dedupe_keep_order(
            [item.strip() for item in chain_env.split(",") if item.strip()]
        )

    primary = resolve_model(role_key, default)
    defaults: list[str] = [primary]

    fallback_env = _clean_model_name(os.getenv("MODEL_FALLBACK_CHAIN"))
    if fallback_env:
        defaults.extend([item.strip() for item in fallback_env.split(",") if item.strip()])
    else:
        if "coder" in role_key or "tester" in role_key:
            defaults.extend([
                "gemini/gemini-2.5-flash",
                "ollama/qwen2.5-coder:14b",
                "gemini/gemini-2.5-flash-lite",
            ])
        elif "lead" in role_key or "validator" in role_key:
            defaults.extend([
                "gemini/gemini-2.5-flash",
                "gemini/gemini-2.5-flash-lite",
                "ollama/qwen2.5-coder:14b",
            ])
        else:
            defaults.extend([
                "gemini/gemini-2.5-flash-lite",
                "gemini/gemini-2.5-flash",
                "ollama/qwen2.5-coder:14b",
            ])

    return _dedupe_keep_order(defaults)


def _is_quota_like_error(error: Exception) -> bool:
    message = str(error).lower()
    tokens = (
        "quota",
        "rate limit",
        "resource exhausted",
        "too many requests",
        "429",
        "limit exceeded",
        "usage limit",
        "503",
        "unavailable",
        "overloaded",
    )
    return any(token in message for token in tokens)


def _is_model_unavailable_error(error: Exception) -> bool:
    message = str(error).lower()
    tokens = (
        "not found",
        "not supported",
        "unsupported",
        "model_not_found",
        "404",
        "available models",
    )
    return any(token in message for token in tokens)


def _fallback_debug_enabled() -> bool:
    return os.getenv("FALLBACK_DEBUG", "1").strip().lower() not in {"0", "false", "no"}


def _log_fallback(message: str) -> None:
    if _fallback_debug_enabled():
        log_fallback_event("fallback", message)


class QuotaAwareFallbackLLM(BaseLLM):
    models: list[str]
    cooldown_seconds: int = 900
    llm_type: str = "fallback"
    provider: str = "openai"

    _clients: dict[str, LLM] = PrivateAttr(default_factory=dict)
    _cooldowns: dict[str, float] = PrivateAttr(default_factory=dict)

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)
        stop_words = ["Observation:", "[No observation", "\n["]
        for model_name in self.models:
            kwargs = {"model": model_name, "temperature": 0.1, "stop": stop_words}
            self._clients[model_name] = LLM(**kwargs)

    def _is_available(self, model_name: str) -> bool:
        cooldown_until = self._cooldowns.get(model_name)
        if cooldown_until is None:
            return True
        return time.time() >= cooldown_until

    def _mark_cooldown(self, model_name: str) -> None:
        self._cooldowns[model_name] = time.time() + self.cooldown_seconds
        _log_fallback(
            f"model cooldown set: {model_name} for {self.cooldown_seconds}s"
        )

    def call(
        self,
        messages: str | list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        callbacks: list[Any] | None = None,
        available_functions: dict[str, Any] | None = None,
        from_task: Any | None = None,
        from_agent: Any | None = None,
        response_model: type[Any] | None = None,
    ) -> str | Any:
        last_error: Exception | None = None

        ordered_models = [model_name for model_name in self.models if self._is_available(model_name)]
        if not ordered_models:
            ordered_models = list(self.models)

        for model_name in ordered_models:
            client = self._clients[model_name]
            try:
                _log_fallback(f"trying model: {model_name}")
                
                # Ajan çağrısını yap
                raw_result = client.call(
                    messages,
                    tools=tools,
                    callbacks=callbacks,
                    available_functions=available_functions,
                    from_task=from_task,
                    from_agent=from_agent,
                    response_model=response_model,
                )

                return raw_result
            except Exception as error:  # pragma: no cover - depends on provider responses
                last_error = error
                if _is_quota_like_error(error) or _is_model_unavailable_error(error):
                    _log_fallback(
                        f"fallbackable error on {model_name}; switching to next model. error={str(error)[:220]}"
                    )
                    self._mark_cooldown(model_name)
                    continue
                _log_fallback(
                    f"non-fallback error on {model_name}; aborting chain. error={str(error)[:220]}"
                )
                raise

        if last_error is not None:
            raise last_error
        raise RuntimeError("No available models in fallback chain")


def build_llm(role_key: str, default: str | None = None, *, enable_fallback: bool = False) -> str | BaseLLM:
    stop_words = ["Observation:", "[No observation", "\n["]

    def _create_llm(model_name: str) -> LLM:
        kwargs = {"model": model_name, "temperature": 0.1, "stop": stop_words}
        return LLM(**kwargs)

    if not enable_fallback:
        return _create_llm(resolve_model(role_key, default))

    chain = resolve_model_chain(role_key, default)
    if len(chain) == 1:
        return _create_llm(chain[0])

    cooldown_seconds = int(os.getenv("MODEL_QUOTA_COOLDOWN_SECONDS", "900"))
    return QuotaAwareFallbackLLM(
        model=chain[0],
        models=chain,
        cooldown_seconds=cooldown_seconds,
    )