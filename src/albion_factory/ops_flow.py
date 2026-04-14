from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import TypedDict

from pydantic import BaseModel, Field
from crewai.flow.flow import Flow, listen, router, start

from albion_factory.fallback_logger import log_fallback_event
from albion_factory.ops_crew import AlbionOpsCrew
from albion_factory.run_registry import create_run_id, ensure_workspace_structure, write_json


class LeadDecision(BaseModel):
    summary: str
    needs_research: bool = False
    needs_data_collection: bool = False
    needs_testing: bool = True
    target_paths: list[str] = Field(default_factory=list)
    test_commands: list[str] = Field(default_factory=list)
    data_urls: list[str] = Field(default_factory=list)
    output_paths: list[str] = Field(default_factory=list)


class ResearchOutput(BaseModel):
    context_summary: str
    relevant_files: list[str] = Field(default_factory=list)
    findings: list[str] = Field(default_factory=list)
    suggested_tests: list[str] = Field(default_factory=list)


class DataOutput(BaseModel):
    collected_sources: list[str] = Field(default_factory=list)
    saved_files: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class TestOutput(BaseModel):
    verdict: str
    commands_run: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    findings: list[str] = Field(default_factory=list)


class ValidationOutput(BaseModel):
    verdict: str
    reason: str
    commit_ready: bool = False
    evidence_used: list[str] = Field(default_factory=list)
    risky_points: list[str] = Field(default_factory=list)
    required_fixes: list[str] = Field(default_factory=list)


class OpsState(TypedDict, total=False):
    ops_request: str
    run_id: str
    report_dir: str
    lead: dict
    research: dict
    data: dict
    test: dict
    validation: dict
    retry_count: int


DEFAULT_TEST_COMMANDS = [
    "uv run python -m compileall src",
]


def _sanitize_test_commands(commands: list[str] | None) -> list[str]:
    if not commands:
        return DEFAULT_TEST_COMMANDS.copy()

    safe_prefixes = (
        "uv run python",
        "uv run pytest",
        "uv run python -m pytest",
        "python",
        "pytest",
        "git diff",
        "git log",
    )
    disallowed_tokens = ("|", "&&", "||", ";", " xargs ", " sh ", " bash ")
    cleaned: list[str] = []
    for command in commands:
        lowered = f" {command.lower()} "
        if any(token in lowered for token in disallowed_tokens):
            continue
        if any(command.startswith(prefix) for prefix in safe_prefixes):
            cleaned.append(command)

    if not cleaned:
        return DEFAULT_TEST_COMMANDS.copy()
    return cleaned


def _normalize_validation_from_test(state: OpsState) -> dict:
    test_payload = state.get("test", {})
    validation_payload = state.get("validation", {})
    test_verdict = str(test_payload.get("verdict", "FAIL")).upper()

    if test_verdict.startswith("PASS") or test_verdict == "TEST PASSED":
        validation_payload["verdict"] = "PASS"
        validation_payload["commit_ready"] = True
        validation_payload.setdefault("reason", "Test çıktısı başarılı ve bloklayıcı bulgu yok.")
        validation_payload.setdefault("evidence_used", test_payload.get("evidence", []))
        validation_payload.setdefault("required_fixes", [])
        validation_payload.setdefault("risky_points", [])
    else:
        validation_payload["verdict"] = validation_payload.get("verdict", "FAIL")
        validation_payload["commit_ready"] = False
        validation_payload.setdefault("reason", "Test çıktısı başarısız veya yetersiz.")

    return validation_payload


def _build_final_summary(state: OpsState, status: str) -> dict:
    return {
        "status": status,
        "ops_request": state.get("ops_request", ""),
        "lead_summary": state.get("lead", {}).get("summary", ""),
        "research_used": bool(state.get("research")),
        "data_collection_used": bool(state.get("data")),
        "test_verdict": state.get("test", {}).get("verdict", ""),
        "validator_verdict": state.get("validation", {}).get("verdict", ""),
        "commit_ready": state.get("validation", {}).get("commit_ready", False),
        "validator_evidence": state.get("validation", {}).get("evidence_used", []),
        "required_fixes": state.get("validation", {}).get("required_fixes", []),
    }


def _read_fallback_events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    events: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except Exception:
            continue
    return events


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _write_markdown(path: Path, title: str, payload: dict | str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(payload, str):
        content = payload
    else:
        lines = [f"# {title}", ""]
        for key, value in payload.items():
            lines.append(f"## {key}")
            if isinstance(value, list):
                if value:
                    lines.extend(f"- {item}" for item in value)
                else:
                    lines.append("- none")
            else:
                lines.append(str(value))
            lines.append("")
        content = "\n".join(lines).strip() + "\n"
    path.write_text(content, encoding="utf-8")


class AlbionOpsFlow(Flow[OpsState]):
    MAX_RETRIES = 0

    @start()
    def request_intake(self):
        ensure_workspace_structure()
        if "ops_request" not in self.state:
            self.state["ops_request"] = "Validate recent implementation using repo, tests and evidence"
        self.state["retry_count"] = 0
        self.state["run_id"] = create_run_id()
        report_dir = Path("reports") / self.state["run_id"]
        report_dir.mkdir(parents=True, exist_ok=True)
        self.state["report_dir"] = str(report_dir)
        os.environ["FALLBACK_EVENT_LOG"] = str(report_dir / "fallback_events.jsonl")
        request_path = report_dir / "request.md"
        request_path.write_text(self.state["ops_request"], encoding="utf-8")
        log_fallback_event("flow", f"ops flow started: {self.state['run_id']}")
        return self.state

    @listen(request_intake)
    def lead_manager(self, _state):
        crew = AlbionOpsCrew()
        result = crew.lead_manager().kickoff(
            self.state["ops_request"],
            response_format=LeadDecision,
        )
        payload = result.pydantic.model_dump() if result.pydantic else {"summary": result.raw}
        payload["test_commands"] = _sanitize_test_commands(payload.get("test_commands"))
        if not payload.get("target_paths"):
            payload["target_paths"] = ["src", "scripts", "sql", "reference"]
        self.state["lead"] = payload
        _write_markdown(Path(self.state["report_dir"]) / "lead_report.md", "Lead Report", payload)
        return payload

    @router(lead_manager)
    def route_after_lead(self, lead_payload):
        if lead_payload.get("needs_research"):
            return "research"
        if lead_payload.get("needs_data_collection"):
            return "data"
        return "test"

    @listen("research")
    def researcher(self, _label):
        crew = AlbionOpsCrew()
        result = crew.researcher().kickoff(
            f"Request: {self.state['ops_request']}\nLead Summary: {self.state['lead'].get('summary','')}\n"
            f"Target Paths: {self.state['lead'].get('target_paths', [])}",
            response_format=ResearchOutput,
        )
        payload = result.pydantic.model_dump() if result.pydantic else {"context_summary": result.raw}
        self.state["research"] = payload
        _write_markdown(Path(self.state["report_dir"]) / "research_report.md", "Research Report", payload)
        return payload

    @router(researcher)
    def route_after_research(self, _payload):
        if self.state["lead"].get("needs_data_collection"):
            return "data"
        return "test"

    @listen("data")
    def data_collector(self, _label):
        crew = AlbionOpsCrew()
        result = crew.data_collector().kickoff(
            f"Request: {self.state['ops_request']}\nURLs: {self.state['lead'].get('data_urls', [])}\n"
            f"Output Paths: {self.state['lead'].get('output_paths', [])}",
            response_format=DataOutput,
        )
        payload = result.pydantic.model_dump() if result.pydantic else {"notes": [result.raw]}
        self.state["data"] = payload
        _write_markdown(Path(self.state["report_dir"]) / "data_report.md", "Data Report", payload)
        return payload

    @listen("test")
    @listen(data_collector)
    def tester(self, _payload):
        crew = AlbionOpsCrew()
        commands = _sanitize_test_commands(self.state["lead"].get("test_commands"))
        result = crew.tester().kickoff(
            f"Request: {self.state['ops_request']}\n"
            f"Lead Output: {json.dumps(self.state.get('lead', {}), ensure_ascii=False)}\n"
            f"Research Output: {json.dumps(self.state.get('research', {}), ensure_ascii=False)}\n"
            f"Run these commands if safe: {commands}\n"
            "Return output with these headings: Commands, Evidence, Findings, Verdict.",
            response_format=TestOutput,
        )
        payload = result.pydantic.model_dump() if result.pydantic else {
            "verdict": "FAIL",
            "findings": [result.raw],
            "evidence": [],
            "commands_run": commands,
        }
        if not payload.get("commands_run"):
            payload["commands_run"] = commands
        if not payload.get("evidence"):
            payload["evidence"] = [f"commands_planned={commands}"]
        self.state["test"] = payload
        _write_markdown(Path(self.state["report_dir"]) / "test_report.md", "Test Report", payload)
        return payload

    @listen(tester)
    def validator(self, _payload):
        crew = AlbionOpsCrew()
        result = crew.validator().kickoff(
            f"Request: {self.state['ops_request']}\n"
            f"Lead: {json.dumps(self.state.get('lead', {}), ensure_ascii=False)}\n"
            f"Research: {json.dumps(self.state.get('research', {}), ensure_ascii=False)}\n"
            f"Data: {json.dumps(self.state.get('data', {}), ensure_ascii=False)}\n"
            f"Test: {json.dumps(self.state.get('test', {}), ensure_ascii=False)}\n"
            "Return output with these headings: Verdict, Evidence Used, Risks, Required Fixes, Commit Ready.",
            response_format=ValidationOutput,
        )
        payload = result.pydantic.model_dump() if result.pydantic else {
            "verdict": "FAIL",
            "reason": result.raw,
            "commit_ready": False,
            "evidence_used": self.state.get("test", {}).get("evidence", []),
        }
        self.state["validation"] = payload
        payload = _normalize_validation_from_test(self.state)
        self.state["validation"] = payload
        _write_markdown(Path(self.state["report_dir"]) / "validator_report.md", "Validator Report", payload)
        return payload

    @router(validator)
    def route_validation(self, validation_payload):
        verdict = str(validation_payload.get("verdict", "FAIL")).upper()
        if verdict == "PASS":
            return "pass"
        retry_count = self.state.get("retry_count", 0)
        if retry_count < self.MAX_RETRIES:
            self.state["retry_count"] = retry_count + 1
            return "retry"
        return "fail"

    @listen("pass")
    @listen("fail")
    def finalize(self, label):
        status = "success" if label == "pass" else "failed"
        final_summary = _build_final_summary(self.state, status)
        _write_markdown(Path(self.state["report_dir"]) / "operational_report.md", "Operational Report", final_summary)
        fallback_events = _read_fallback_events(Path(self.state["report_dir"]) / "fallback_events.jsonl")
        manifest = {
            "run_id": self.state["run_id"],
            "status": status,
            "started_at": _utc_now(),
            "finished_at": _utc_now(),
            "ops_request": self.state["ops_request"],
            "artifacts": [
                "request.md",
                "lead_report.md",
                "research_report.md",
                "data_report.md",
                "test_report.md",
                "validator_report.md",
                "operational_report.md",
            ],
            "validator": self.state.get("validation", {}),
            "fallback_summary": {
                "event_count": len(fallback_events),
                "recent_messages": [event.get("message", "") for event in fallback_events[-10:]],
            },
        }
        write_json(Path(self.state["report_dir"]) / "manifest.json", manifest)
        return manifest


def kickoff(ops_request: str):
    flow = AlbionOpsFlow()
    flow.state["ops_request"] = ops_request
    return flow.kickoff()