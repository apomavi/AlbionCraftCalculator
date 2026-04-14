from __future__ import annotations

import json
import re
from typing import TypedDict

from crewai.flow.flow import Flow, listen, router, start

from albion_factory.crew import AlbionFactory


class ProductionState(TypedDict, total=False):
    project_goal: str
    lead_output: str
    research_output: str
    data_collector_output: str
    coder_output: str
    tester_output: str
    validator_output: str
    feedback_target: str
    feedback_reason: str
    retry_counts: dict[str, int]
    feedback_history: list[dict[str, str]]
    final_status: str


class AlbionProductionFlow(Flow[ProductionState]):
    MAX_RETRIES_PER_AGENT = 5

    def _normalize_feedback_target(self, value: str) -> str:
        lowered = value.strip().lower()
        if lowered in {"researcher", "data_collector", "coder", "tester", "validator", "none"}:
            return lowered
        if "research" in lowered:
            return "researcher"
        if "data" in lowered or "collector" in lowered:
            return "data_collector"
        if "coder" in lowered or "code" in lowered:
            return "coder"
        if "tester" in lowered or "test" in lowered:
            return "tester"
        if "valid" in lowered:
            return "validator"
        return "none"

    def _is_raw_tool_dump(self, text: str) -> bool:
        normalized = text.strip()
        if not normalized:
            return True
        json_like = normalized.startswith("{") or normalized.startswith("```json")
        tool_markers = [
            '"name"',
            '"function_name"',
            '"arguments"',
            'Action Input:',
        ]
        return json_like and any(marker in normalized for marker in tool_markers)

    def _contains_embedded_tool_dump(self, text: str) -> bool:
        lowered = text.lower()
        has_qwen_dump = ("write_repo_file" in lowered or "read_repo_file" in lowered or "verify_text_structure" in lowered) and "{" in lowered and '"' in lowered
        return (
            ('### commands:' in lowered and '"arguments"' in lowered) or
            ('## commands' in lowered and '"arguments"' in lowered) or
            has_qwen_dump
        )

    def _safe_kickoff(self, agent_name: str, agent_instance, prompt: str) -> str:
        try:
            result = agent_instance.kickoff(prompt)
            return getattr(result, "raw", str(result))
        except Exception as exc:
            return (
                f"AGENT CRASHED ({agent_name}): {str(exc)}\n\n"
                f"CRITICAL ERROR: The {agent_name} agent crashed or returned an empty response. "
                f"The Validator MUST mark this run as FAIL and set Feedback Target to '{agent_name}' so it can retry."
            )

    @start()
    def request_intake(self):
        if "project_goal" not in self.state:
            self.state["project_goal"] = "No request provided"
        self.state.setdefault("retry_counts", {})
        self.state.setdefault("feedback_history", [])
        return self.state

    @router(request_intake)
    def route_intake(self, _):
        return "route_to_lead"

    @listen("route_to_lead")
    def lead(self, _state):
        raw = self._safe_kickoff("lead", AlbionFactory().lead(), self.state["project_goal"])
        self.state["lead_output"] = raw
        return raw

    @router(lead)
    def route_lead(self, _):
        return "route_to_researcher"

    @listen("route_to_researcher")
    def researcher(self, _input):
        prompt = self._build_prompt_for_agent(
            agent_name="researcher",
            base_output=self.state.get("lead_output", ""),
        )
        raw = self._safe_kickoff("researcher", AlbionFactory().researcher(), prompt)
        self.state["research_output"] = raw
        return raw

    @router(researcher)
    def route_researcher(self, _):
        return "route_to_data_collector"

    @listen("route_to_data_collector")
    def data_collector(self, _input):
        prompt = self._build_prompt_for_agent(
            agent_name="data_collector",
            base_output=self.state.get("research_output", ""),
        )
        raw = self._safe_kickoff("data_collector", AlbionFactory().data_collector(), prompt)
        self.state["data_collector_output"] = raw
        return raw

    @router(data_collector)
    def route_data_collector(self, _):
        return "route_to_coder"

    @listen("route_to_coder")
    def coder(self, _input):
        prompt = self._build_prompt_for_agent(
            agent_name="coder",
            base_output=f"Research:\n{self.state.get('research_output', '')}\n\nData Collection:\n{self.state.get('data_collector_output', '')}",
        )
        raw = self._safe_kickoff("coder", AlbionFactory().coder(), prompt)
        normalized = self._normalize_agent_output("coder", raw)
        self.state["coder_output"] = normalized
        return normalized

    @router(coder)
    def route_coder(self, _):
        return "route_to_tester"

    @listen("route_to_tester")
    def tester(self, _input):
        prompt = self._build_prompt_for_agent(
            agent_name="tester",
            base_output=self.state.get("coder_output", ""),
        )
        raw = self._safe_kickoff("tester", AlbionFactory().tester(), prompt)
        normalized = self._normalize_agent_output("tester", raw)
        self.state["tester_output"] = normalized
        return normalized

    @router(tester)
    def route_tester(self, _):
        return "route_to_validator"

    @listen("route_to_validator")
    def validator(self, _input):
        prompt = (
            f"Project Goal:\n{self.state['project_goal']}\n\n"
            f"Lead Output:\n{self.state.get('lead_output', '')}\n\n"
            f"Research Output:\n{self.state.get('research_output', '')}\n\n"
            f"Data Collector Output:\n{self.state.get('data_collector_output', '')}\n\n"
            f"Coder Output:\n{self.state.get('coder_output', '')}\n\n"
            f"Tester Output:\n{self.state.get('tester_output', '')}"
        )
        raw = self._safe_kickoff("validator", AlbionFactory().validator(), prompt)
        normalized = self._normalize_validator_output(raw)
        self.state["validator_output"] = normalized
        self._extract_feedback_fields(normalized)
        return normalized

    @router(validator)
    def route_after_validation(self, _validator_output):
        verdict = self.state.get("validator_output", "").upper()
        feedback_target = self.state.get("feedback_target", "none").lower()

        # Validator self-correction for missing headers using deterministic flag
        if self.state.get("validator_format_failed", False):
            self.state["feedback_target"] = "validator"
            self.state["feedback_reason"] = "You failed to use the required markdown headers (Verdict, Evidence Used, Risks, Required Fixes, Feedback Target, Feedback Reason, Commit Ready). You must rewrite your evaluation using EXACTLY these headers."
            self.state.setdefault("feedback_history", []).append(
                {
                    "target": "validator",
                    "reason": self.state["feedback_reason"],
                }
            )
            feedback_target = "validator"

        tester_output = self.state.get("tester_output", "")
        if self._is_raw_tool_dump(tester_output) or self._contains_embedded_tool_dump(tester_output):
            self.state["feedback_target"] = "tester"
            self.state["feedback_reason"] = "Tester output still contained raw tool-call data instead of a clean human-readable evidence summary."
            self.state.setdefault("feedback_history", []).append(
                {
                    "target": "tester",
                    "reason": self.state["feedback_reason"],
                }
            )
            feedback_target = "tester"

        if self._is_raw_tool_dump(self.state.get("coder_output", "")):
            self.state["feedback_target"] = "coder"
            self.state["feedback_reason"] = "Coder final output was a raw tool-call dump instead of an implementation summary."
            self.state.setdefault("feedback_history", []).append(
                {
                    "target": "coder",
                    "reason": self.state["feedback_reason"],
                }
            )
            feedback_target = "coder"

        is_pass = "VERDICT\nPASS" in verdict or "VERDICT: PASS" in verdict
        is_commit_ready = "COMMIT READY: YES" in verdict or "COMMIT READY\nYES" in verdict

        if is_pass and is_commit_ready:
            self.state["final_status"] = "PASS"
            return "route_finalize_pass"

        if feedback_target in {"researcher", "data_collector", "coder", "tester", "validator"}:
            retry_counts = self.state.setdefault("retry_counts", {})
            current = retry_counts.get(feedback_target, 0)
            if current < self.MAX_RETRIES_PER_AGENT:
                retry_counts[feedback_target] = current + 1
                return f"route_to_{feedback_target}"

        self.state["final_status"] = "FAIL"
        return "route_finalize_fail"

    @listen("route_finalize_pass")
    def finalize_pass(self, _label):
        return {
            "status": "PASS",
            "lead_output": self.state.get("lead_output", ""),
            "research_output": self.state.get("research_output", ""),
            "data_collector_output": self.state.get("data_collector_output", ""),
            "coder_output": self.state.get("coder_output", ""),
            "tester_output": self.state.get("tester_output", ""),
            "validator_output": self.state.get("validator_output", ""),
            "feedback_history": self.state.get("feedback_history", []),
            "retry_counts": self.state.get("retry_counts", {}),
        }

    @listen("route_finalize_fail")
    def finalize_fail(self, _label):
        return {
            "status": "FAIL",
            "lead_output": self.state.get("lead_output", ""),
            "research_output": self.state.get("research_output", ""),
            "data_collector_output": self.state.get("data_collector_output", ""),
            "coder_output": self.state.get("coder_output", ""),
            "tester_output": self.state.get("tester_output", ""),
            "validator_output": self.state.get("validator_output", ""),
            "feedback_history": self.state.get("feedback_history", []),
            "retry_counts": self.state.get("retry_counts", {}),
        }

    def _extract_feedback_fields(self, text: str) -> None:
        feedback_target = self._extract_field(text, "Feedback Target") or "none"
        feedback_reason = self._extract_field(text, "Feedback Reason") or ""
        self.state["feedback_target"] = self._normalize_feedback_target(feedback_target)
        self.state["feedback_reason"] = feedback_reason.strip()
        self.state.setdefault("feedback_history", []).append(
            {
                "target": self.state["feedback_target"],
                "reason": self.state["feedback_reason"],
            }
        )

    def _normalize_validator_output(self, text: str) -> str:
        verdict = self._extract_field(text, "Verdict")
        evidence = self._extract_field(text, "Evidence Used")
        risks = self._extract_field(text, "Risks")
        fixes = self._extract_field(text, "Required Fixes")
        feedback_target_raw = self._extract_field(text, "Feedback Target")
        feedback_reason = self._extract_field(text, "Feedback Reason")
        commit_ready = self._extract_field(text, "Commit Ready")

        # Validator'ı serbest bırak (Kendi kendine ceza kesmesin)
        self.state["validator_format_failed"] = False

        verdict = verdict or "FAIL"
        evidence = evidence or "No structured evidence provided"
        risks = risks or "Validator returned unstructured risks section"
        fixes = fixes or "Provide validator output in required contract format"
        feedback_target = self._normalize_feedback_target(feedback_target_raw or "none")
        feedback_reason = feedback_reason or "Validator output did not follow required structured format"
        commit_ready = commit_ready or "NO"

        return (
            f"## Verdict\n{verdict}\n\n"
            f"## Evidence Used\n{evidence}\n\n"
            f"## Risks\n{risks}\n\n"
            f"## Required Fixes\n{fixes}\n\n"
            f"## Feedback Target\n{feedback_target}\n\n"
            f"## Feedback Reason\n{feedback_reason}\n\n"
            f"## Commit Ready\n{commit_ready}\n"
        )

    def _extract_field(self, text: str, field_name: str) -> str | None:
        # Birden fazla cümleyi (multiline) diğer başlığa kadar yakalar
        pattern = re.compile(
            rf"(?:##\s*{re.escape(field_name)}|{re.escape(field_name)}\s*[:\n])\s*(.*?)(?=(?:##\s*[A-Z]|\n[A-Z][a-z\s]+:|\Z))",
            re.IGNORECASE | re.DOTALL
        )
        match = pattern.search(text)
        return match.group(1).strip() if match else None

    def _build_prompt_for_agent(self, agent_name: str, base_output: str) -> str:
        feedback_target = self.state.get("feedback_target", "")
        feedback_reason = self.state.get("feedback_reason", "")
        prompt = f"Project Goal:\n{self.state['project_goal']}\n\nPrevious Context:\n{base_output}"
        if feedback_target == agent_name and feedback_reason:
            prompt += f"\n\nFeedback To Address:\n{feedback_reason}"
            prompt += (
                "\n\nImportant: Your next final answer must be human-readable markdown only. "
                "Do not output raw tool-call JSON, function call objects, or bare arguments."
            )
        prompt += (
            "\n\nSTRICT INSTRUCTION: When you are ready to provide your Final Answer, you must strictly output the requested markdown headers from your system prompt contract.\n"
        )
        if agent_name in ("researcher", "data_collector", "coder", "tester"):
            prompt += (
                "If you need to use a tool, you MUST use EXACTLY this plain text format (do not use markdown blocks):\n"
                "Action: tool_name\n"
                "Action Input: {\"parameter_name\": \"value\"}\n\n"
                "Your Action Input MUST be exactly one JSON object starting with { and ending with }. Do not use empty lists [].\n"
                "CRITICAL: You MUST halt all text generation immediately after outputting the } character of your Action Input.\n"
            )
        prompt += "Never put tool calls inside your Final Answer."
        return prompt

    def _normalize_agent_output(self, agent_name: str, text: str) -> str:
        if not self._is_raw_tool_dump(text):
            return text

        parsed = self._try_parse_tool_dump(text)
        if not parsed:
            return text

        if agent_name == "coder":
            path = parsed.get("arguments", {}).get("path", "unknown")
            return (
                "## Target Files\n"
                f"- {path}\n\n"
                "## Planned Changes\n"
                f"- Tool call `{parsed.get('name', parsed.get('function_name', 'unknown'))}` prepared for implementation\n\n"
                "## Applied Changes\n"
                "- Tool output was captured and normalized by flow\n\n"
                "## Remaining Risks\n"
                "- Agent returned raw tool-call dump; manual review still recommended\n"
            )

        if agent_name == "tester":
            path = parsed.get("arguments", {}).get("path", "unknown")
            return (
                "## Commands\n"
                f"- Verification requested for `{path}`\n\n"
                "## Evidence\n"
                f"- Raw tool invocation `{parsed.get('name', parsed.get('function_name', 'unknown'))}` was detected and normalized\n\n"
                "## Findings\n"
                "- Tester returned a raw tool-call dump instead of a final evidence summary\n\n"
                "## Verdict\n"
                "FAIL\n"
            )

        return text

    def _try_parse_tool_dump(self, text: str) -> dict | None:
        normalized = text.strip()
        if normalized.startswith("```json"):
            normalized = normalized.removeprefix("```json").removesuffix("```").strip()
        try:
            parsed = json.loads(normalized)
        except Exception:
            return None
        return parsed if isinstance(parsed, dict) else None


def kickoff(project_goal: str):
    flow = AlbionProductionFlow()
    flow.state["project_goal"] = project_goal
    return flow.kickoff()