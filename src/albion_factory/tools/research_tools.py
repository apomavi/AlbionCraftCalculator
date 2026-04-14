from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Type
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

from crewai.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr

from albion_factory.fallback_logger import log_fallback_event


def _is_quota_like_error_message(message: str) -> bool:
    lowered = message.lower()
    tokens = (
        "quota",
        "rate limit",
        "resource exhausted",
        "too many requests",
        "429",
        "limit exceeded",
        "usage limit",
    )
    return any(token in lowered for token in tokens)


def _fallback_debug_enabled() -> bool:
    return os.getenv("FALLBACK_DEBUG", "1").strip().lower() not in {"0", "false", "no"}


def _log_search_fallback(message: str) -> None:
    if _fallback_debug_enabled():
        log_fallback_event("search-fallback", message)


def _dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


class SmartResearchInput(BaseModel):
    query: str = Field(..., description="Research query")
    official_urls: list[str] = Field(
        default_factory=list,
        description="Optional official source URLs to fetch directly when search is limited",
    )
    local_paths: list[str] = Field(
        default_factory=lambda: ["knowledge", "reference", "requests", "reports"],
        description="Optional repo paths for local fallback search",
    )


class SmartResearchTool(BaseTool):
    name: str = "smart_research"
    description: str = (
        "Researches a query using a fallback chain: Serper search, direct official URL fetch, "
        "and local repository knowledge search."
    )
    args_schema: Type[BaseModel] = SmartResearchInput

    _cooldowns: dict[str, float] = PrivateAttr(default_factory=dict)

    def _run(
        self,
        query: str,
        official_urls: list[str] | None = None,
        local_paths: list[str] | None = None,
    ) -> str:
        search_chain = self._resolve_search_chain()
        official_urls = official_urls or []
        local_paths = local_paths or ["knowledge", "reference", "requests", "reports"]

        results: list[dict[str, object]] = []
        errors: list[dict[str, str]] = []

        for step in search_chain:
            if not self._is_available(step):
                continue
            try:
                if step == "serper":
                    serper_results = self._search_with_serper(query)
                    if serper_results:
                        results.append({"source": "serper", "items": serper_results})
                        break
                elif step == "direct_fetch":
                    fetched = self._fetch_official_urls(official_urls)
                    if fetched:
                        results.append({"source": "direct_fetch", "items": fetched})
                        break
                elif step == "local_knowledge":
                    local = self._search_local_knowledge(query, local_paths)
                    if local:
                        results.append({"source": "local_knowledge", "items": local})
                        break
            except Exception as error:  # pragma: no cover - network/provider dependent
                errors.append({"step": step, "error": str(error)})
                if _is_quota_like_error_message(str(error)):
                    self._mark_cooldown(step)
                    continue

        return json.dumps(
            {
                "query": query,
                "search_chain": search_chain,
                "results": results,
                "errors": errors,
            },
            ensure_ascii=False,
        )

    def _resolve_search_chain(self) -> list[str]:
        raw = os.getenv("SEARCH_CHAIN", "serper,direct_fetch,local_knowledge")
        return _dedupe_keep_order([item.strip() for item in raw.split(",") if item.strip()])

    def _is_available(self, step: str) -> bool:
        cooldown_until = self._cooldowns.get(step)
        if cooldown_until is None:
            return True
        return time.time() >= cooldown_until

    def _mark_cooldown(self, step: str) -> None:
        cooldown_seconds = int(os.getenv("SEARCH_QUOTA_COOLDOWN_SECONDS", "900"))
        self._cooldowns[step] = time.time() + cooldown_seconds
        _log_search_fallback(f"step cooldown set: {step} for {cooldown_seconds}s")

    def _search_with_serper(self, query: str) -> list[dict[str, str]]:
        api_key = os.getenv("SERPER_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError("SERPER_API_KEY is missing")

        body = json.dumps({"q": query, "num": 5}).encode("utf-8")
        request = Request(
            "https://google.serper.dev/search",
            data=body,
            headers={
                "X-API-KEY": api_key,
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urlopen(request) as response:  # nosec - fixed trusted host
            payload = json.loads(response.read().decode("utf-8", errors="ignore"))

        organic = payload.get("organic", [])
        return [
            {
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
            }
            for item in organic[:5]
        ]

    def _fetch_official_urls(self, official_urls: list[str]) -> list[dict[str, str]]:
        items: list[dict[str, str]] = []
        for url in official_urls[:5]:
            if not url.startswith("https://"):
                continue
            with urlopen(url) as response:  # nosec - caller restricted to https urls
                content = response.read().decode("utf-8", errors="ignore")[:4000]
            items.append({"url": url, "content": content})
        return items

    def _search_local_knowledge(self, query: str, local_paths: list[str]) -> list[dict[str, str]]:
        terms = [term for term in re.split(r"\W+", query.lower()) if len(term) >= 3]
        if not terms:
            return []

        matches: list[dict[str, str]] = []
        for local_path in local_paths:
            root = Path(local_path)
            if not root.exists():
                continue
            for file_path in root.rglob("*"):
                if not file_path.is_file():
                    continue
                try:
                    text = file_path.read_text(encoding="utf-8")
                except Exception:
                    continue
                lowered = text.lower()
                if not any(term in lowered for term in terms):
                    continue
                snippet = text[:1000]
                matches.append(
                    {
                        "path": str(file_path).replace("\\", "/"),
                        "snippet": snippet,
                    }
                )
                if len(matches) >= 5:
                    return matches
        return matches


class GeminiWebSearchInput(BaseModel):
    query: str = Field(..., description="Query for a web-search capable Gemini path")


class GeminiWebSearchProbeTool(BaseTool):
    name: str = "gemini_web_search_probe"
    description: str = "Probes whether a Gemini web-search route is configured and usable."
    args_schema: Type[BaseModel] = GeminiWebSearchInput

    def _run(self, query: str) -> str:
        configured_model = os.getenv("SEARCH_MODEL_PRIMARY", "").strip()
        return json.dumps(
            {
                "query": query,
                "configured_model": configured_model,
                "status": "not_implemented",
                "message": (
                    "No verified Gemini web-search tool route is wired yet; fallback should use "
                    "Serper/direct_fetch/local_knowledge."
                ),
            },
            ensure_ascii=False,
        )