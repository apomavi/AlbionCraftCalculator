from __future__ import annotations

import os
import re
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path

from dotenv import load_dotenv

from albion_factory.production_flow import kickoff as production_kickoff
from albion_factory.run_registry import append_csv_row, create_run_id, ensure_workspace_structure, write_json


RUN_INDEX_HEADERS = ["run_id", "request_file", "status", "started_at", "finished_at"]


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _register_run(run_id: str, request_path: Path, status: str, started_at: str, finished_at: str) -> None:
    append_csv_row(
        Path("runs/index.csv"),
        RUN_INDEX_HEADERS,
        {
            "run_id": run_id,
            "request_file": str(request_path).replace("\\", "/"),
            "status": status,
            "started_at": started_at,
            "finished_at": finished_at,
        },
    )


def run(request_file: str | None = None) -> Path:
    load_dotenv()
    ensure_workspace_structure()

    if not request_file:
        raise ValueError("request_file is required")

    request_path = Path(request_file)
    if not request_path.exists():
        raise FileNotFoundError(request_file)
    run_id = create_run_id()
    report_dir = Path("reports") / run_id
    report_dir.mkdir(parents=True, exist_ok=True)

    started_at = _utc_now()
    status = "success"
    request_text = request_path.read_text(encoding="utf-8")

    try:
        result = production_kickoff(request_text)
        finished_at = _utc_now()
        shutil.copy2(request_path, report_dir / "request.md")

        result_preview = str(result)[:2000]
        if isinstance(result, dict):
            status = result.get("status", status).lower()
            result_preview = result.get("validator_output", str(result))[:2000]

            for key, filename in [
                ("lead_output", "lead_report.md"),
                ("research_output", "research_report.md"),
                ("data_collector_output", "data_collector_report.md"),
                ("coder_output", "coder_report.md"),
                ("tester_output", "tester_report.md"),
                ("validator_output", "validator_report.md"),
            ]:
                if result.get(key):
                    (report_dir / filename).write_text(str(result[key]), encoding="utf-8")

            if "feedback_history" in result:
                write_json(report_dir / "feedback_history.json", {"feedback_history": result["feedback_history"], "retry_counts": result.get("retry_counts", {})})

        write_json(
            report_dir / "manifest.json",
            {
                "run_id": run_id,
                "request_file": str(request_path).replace("\\", "/"),
                "started_at": started_at,
                "finished_at": finished_at,
                "status": status,
                "result_preview": result_preview,
                "runner": "scripts/run_request_phase.py",
            },
        )
        _register_run(run_id, request_path, status, started_at, finished_at)
        print(result)
        print(f"Saved to {report_dir}")
        return report_dir
    except Exception as exc:
        status = "failed"
        finished_at = _utc_now()
        shutil.copy2(request_path, report_dir / "request.md")
        write_json(
            report_dir / "manifest.json",
            {
                "run_id": run_id,
                "request_file": str(request_path).replace("\\", "/"),
                "started_at": started_at,
                "finished_at": finished_at,
                "status": status,
                "error": str(exc),
                "runner": "scripts/run_request_phase.py",
            },
        )
        _register_run(run_id, request_path, status, started_at, finished_at)
        raise


if __name__ == "__main__":
    request_arg = sys.argv[1] if len(sys.argv) > 1 else os.getenv("REQUEST_FILE")
    run(request_arg)