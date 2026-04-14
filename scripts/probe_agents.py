from __future__ import annotations

import json
import os
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from dotenv import load_dotenv

from albion_factory.crew import AlbionFactory
from albion_factory.run_registry import ensure_workspace_structure, write_json


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _slug(value: str) -> str:
    return (
        value.lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
    )


def _write_markdown(path: Path, title: str, payload: dict[str, Any]) -> None:
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
    path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def _read_fallback_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except Exception:
            continue
    return events


@dataclass
class AgentProbe:
    crew_name: str
    agent_name: str
    factory: Callable[[], Any]
    prompt: str


def build_probes() -> list[AgentProbe]:
    production = AlbionFactory()

    return [
        AgentProbe(
            crew_name="production",
            agent_name="lead",
            factory=production.lead,
            prompt=(
                "Kısa test. Albion craft calculator isteğini küçük fazlara böl. "
                "Mutlaka şu başlıklarla cevap ver: Scope, Required Agents, Constraints, Success Criteria, Next Task."
            ),
        ),
        AgentProbe(
            crew_name="production",
            agent_name="researcher",
            factory=production.researcher,
            prompt=(
                "Kısa test. Craft calculator için recipe/price/domain bağlamını özetle. "
                "Mutlaka şu başlıklarla cevap ver: Source Inventory, Findings, Constraints, Implementation Notes, Sources."
            ),
        ),
        AgentProbe(
            crew_name="production",
            agent_name="data_collector",
            factory=production.data_collector,
            prompt=(
                "Kısa test. Craft calculator için gerekli fiyat API veri yapısını topla. "
                "Mutlaka şu başlıklarla cevap ver: Target Data, Collected Data, Normalization Notes."
            ),
        ),
        AgentProbe(
            crew_name="production",
            agent_name="coder",
            factory=production.coder,
            prompt=(
                "Kısa test. Küçük bir craft calculator dosya değişikliğini nasıl uygulayacağını anlat. "
                "Mutlaka şu başlıklarla cevap ver: Target Files, Planned Changes, Applied Changes, Remaining Risks."
            ),
        ),
        AgentProbe(
            crew_name="production",
            agent_name="tester",
            factory=production.tester,
            prompt=(
                "Kısa test. Compile ve smoke evidence nasıl üretilir anlat. "
                "Mutlaka şu başlıklarla cevap ver: Commands, Evidence, Findings, Verdict."
            ),
        ),
        AgentProbe(
            crew_name="production",
            agent_name="validator",
            factory=production.validator,
            prompt=(
                "Kısa test. Bir craft calculator değişikliğini nasıl PASS/PARTIAL/FAIL değerlendirirsin? "
                "Mutlaka şu başlıklarla cevap ver: Verdict, Evidence Used, Risks, Required Fixes, Commit Ready."
            ),
        ),
    ]


def run() -> Path:
    load_dotenv()
    ensure_workspace_structure()

    run_id = f"AGENT-PROBE-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
    report_dir = Path("reports") / run_id
    report_dir.mkdir(parents=True, exist_ok=True)
    os.environ["FALLBACK_EVENT_LOG"] = str(report_dir / "fallback_events.jsonl")

    summary: list[dict[str, Any]] = []
    probes = build_probes()

    for probe in probes:
        started_at = _utc_now()
        status = "success"
        raw_output = ""
        error = ""

        try:
            agent = probe.factory()
            result = agent.kickoff(probe.prompt)
            raw_output = getattr(result, "raw", str(result))
        except Exception as exc:  # pragma: no cover - provider/runtime dependent
            status = "failed"
            error = str(exc)

        finished_at = _utc_now()
        item = {
            "crew": probe.crew_name,
            "agent": probe.agent_name,
            "status": status,
            "started_at": started_at,
            "finished_at": finished_at,
            "prompt": probe.prompt,
            "raw_output": raw_output,
            "error": error,
        }
        summary.append(item)

        stem = f"{probe.crew_name}_{probe.agent_name}"
        write_json(report_dir / f"{_slug(stem)}.json", item)
        _write_markdown(report_dir / f"{_slug(stem)}.md", f"Agent Probe - {stem}", item)

    manifest = {
        "run_id": run_id,
        "created_at": _utc_now(),
        "total_agents": len(summary),
        "expected_agents": len(probes),
        "success_count": len([item for item in summary if item["status"] == "success"]),
        "failed_count": len([item for item in summary if item["status"] == "failed"]),
        "completed": len(summary) == len(probes),
        "agents": [{"crew": item["crew"], "agent": item["agent"], "status": item["status"]} for item in summary],
    }

    fallback_log_path = report_dir / "fallback_events.jsonl"
    fallback_events = _read_fallback_events(fallback_log_path)
    kind_counts = Counter(event.get("kind", "unknown") for event in fallback_events)
    manifest["fallback_summary"] = {
        "event_log": str(fallback_log_path).replace("\\", "/"),
        "event_count": len(fallback_events),
        "kind_counts": dict(kind_counts),
        "recent_messages": [event.get("message", "") for event in fallback_events[-8:]],
    }

    write_json(report_dir / "manifest.json", manifest)
    _write_markdown(report_dir / "summary.md", "Agent Probe Summary", manifest)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"Saved to {report_dir}")
    return report_dir


if __name__ == "__main__":
    run()