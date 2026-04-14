from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from albion_factory.run_registry import write_json


@dataclass
class ScoreBreakdown:
    execution_score: int
    relevance_score: int
    structure_score: int
    clarity_score: int
    penalty_score: int

    @property
    def total(self) -> int:
        return max(
            0,
            min(
                100,
                self.execution_score
                + self.relevance_score
                + self.structure_score
                + self.clarity_score
                - self.penalty_score,
            ),
        )


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _word_count(text: str) -> int:
    return len([token for token in text.split() if token.strip()])


def _score_item(payload: dict[str, Any]) -> dict[str, Any]:
    raw_output = str(payload.get("raw_output", "") or "")
    error = str(payload.get("error", "") or "")
    prompt = str(payload.get("prompt", "") or "")

    execution = 35 if payload.get("status") == "success" else 0
    relevance = 0
    structure = 0
    clarity = 0
    penalty = 0
    notes: list[str] = []
    role = str(payload.get("agent", "") or "")

    if raw_output.strip():
        relevance += 20
    else:
        notes.append("Boş çıktı")
        penalty += 20

    if _word_count(raw_output) >= 12:
        clarity += 15
    elif _word_count(raw_output) >= 5:
        clarity += 8
    else:
        notes.append("Çıktı çok kısa")
        penalty += 10

    lower_output = raw_output.lower()
    lower_prompt = prompt.lower()
    if any(token in lower_output for token in ["pass", "fail", "partial", "scope", "reason", "next", "test", "source"]):
        structure += 15
    elif any(token in lower_prompt for token in ["3 maddede", "kısa", "nasıl", "değerlendir"]):
        structure += 8

    if any(token in lower_output for token in ["albion", "aodp", "repo", "csv", "test", "validator", "research"]):
        relevance += 20
    else:
        notes.append("Göreve zayıf bağ")
        penalty += 10

    if raw_output.strip().startswith("{") and '"arguments": {}' in raw_output:
        notes.append("Araç çağrısı benzeri anlamsız boş çıktı")
        penalty += 25

    if '"name": "_chat"' in raw_output:
        notes.append("Araç sarmalı çıktı; kabul edilebilir ama izlenmeli")

    if "there is no official source" in lower_output and "aodp" in lower_prompt:
        notes.append("Muhtemel yanlış araştırma sonucu")
        penalty += 15

    if error.strip():
        notes.append(f"Hata kaydı var: {error[:160]}")
        penalty += 10

    # Role-specific scoring
    if role in {"validator"}:
        required = ["verdict", "reason", "fix", "risk", "claim", "evidence"]
        if any(token in lower_output for token in required):
            structure += 10
        else:
            notes.append("Validator çıktısında beklenen alanlar zayıf")
            penalty += 10
    elif role in {"tester"}:
        required = ["verdict", "test", "command", "evidence", "finding"]
        if any(token in lower_output for token in required):
            structure += 10
        else:
            notes.append("Tester çıktısında beklenen test/evidence alanları zayıf")
            penalty += 10
    elif role in {"researcher"}:
        if any(token in lower_output for token in ["http", "source", "aodp", "albion"]):
            relevance += 10
        else:
            notes.append("Researcher çıktısında kaynak izi zayıf")
            penalty += 10
    elif role in {"data_collector"}:
        required = ["target data", "collected data", "normalization notes", "data"]
        if sum(1 for token in required if token in lower_output) >= 2:
            structure += 10
        else:
            notes.append("Data Collector çıktısında beklenen alanlar zayıf")
            penalty += 10
    elif role in {"lead", "lead_manager"}:
        if any(token in lower_output for token in ["scope", "next", "criteria", "plan"]):
            structure += 10

    breakdown = ScoreBreakdown(
        execution_score=execution,
        relevance_score=relevance,
        structure_score=structure,
        clarity_score=clarity,
        penalty_score=penalty,
    )

    verdict = "GOOD"
    if breakdown.total < 80:
        verdict = "NEEDS_REVIEW"
    if breakdown.total < 60:
        verdict = "WEAK"

    return {
        "crew": payload.get("crew", ""),
        "agent": payload.get("agent", ""),
        "score": breakdown.total,
        "verdict": verdict,
        "breakdown": {
            "execution": breakdown.execution_score,
            "relevance": breakdown.relevance_score,
            "structure": breakdown.structure_score,
            "clarity": breakdown.clarity_score,
            "penalty": breakdown.penalty_score,
        },
        "notes": notes,
        "raw_output_preview": raw_output[:500],
    }


def _write_markdown(path: Path, title: str, items: list[dict[str, Any]]) -> None:
    lines = [f"# {title}", ""]
    for item in items:
        lines.append(f"## {item['crew']} / {item['agent']}")
        lines.append(f"- score: {item['score']}")
        lines.append(f"- verdict: {item['verdict']}")
        for note in item.get("notes", []):
            lines.append(f"- note: {note}")
        lines.append("")
    path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def _build_role_averages(items: list[dict[str, Any]]) -> dict[str, float]:
    buckets: dict[str, list[int]] = {}
    for item in items:
        buckets.setdefault(item["agent"], []).append(int(item["score"]))
    return {role: round(sum(scores) / len(scores), 2) for role, scores in buckets.items()}


def run(report_dir_arg: str | None = None) -> Path:
    if report_dir_arg:
        report_dir = Path(report_dir_arg)
    else:
        candidates = sorted(Path("reports").glob("AGENT-PROBE-*"))
        if not candidates:
            raise SystemExit("No AGENT-PROBE reports found")
        report_dir = candidates[-1]

    manifest_path = report_dir / "manifest.json"
    if manifest_path.exists():
        manifest = _load_json(manifest_path)
        if not manifest.get("completed", False):
            raise SystemExit(f"Probe run not completed yet: {report_dir}")

    items: list[dict[str, Any]] = []
    for json_file in sorted(report_dir.glob("*.json")):
        if json_file.name in {"manifest.json", "agent_quality_scores.json"}:
            continue
        payload = _load_json(json_file)
        if "agent" not in payload:
            continue
        items.append(_score_item(payload))

    summary = {
        "report_dir": str(report_dir).replace("\\", "/"),
        "total_agents": len(items),
        "average_score": round(sum(item["score"] for item in items) / max(len(items), 1), 2),
        "role_averages": _build_role_averages(items),
        "weak_agents": [f"{item['crew']}/{item['agent']}" for item in items if item["score"] < 60],
        "needs_review_agents": [f"{item['crew']}/{item['agent']}" for item in items if 60 <= item["score"] < 80],
        "good_agents": [f"{item['crew']}/{item['agent']}" for item in items if item["score"] >= 80],
        "items": items,
    }

    write_json(report_dir / "agent_quality_scores.json", summary)
    _write_markdown(report_dir / "agent_quality_scores.md", "Agent Quality Scores", items)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return report_dir


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    run(arg)