import json
import os
import shutil
from datetime import datetime
from pathlib import Path

from albion_factory.crew import AlbionFactory
from albion_factory.run_registry import (
    append_csv_row,
    create_run_id,
    ensure_workspace_structure,
    resolve_request_file,
    write_json,
)


RUN_INDEX_HEADERS = ["run_id", "request_file", "status", "started_at", "finished_at"]


def get_request_file() -> Path:
    return resolve_request_file(os.getenv("REQUEST_FILE"))


def copy_reports(output_dir: Path, report_dir: Path) -> list[str]:
    copied_files: list[str] = []
    for filename in ["lead_report.md", "research_report.md", "validator_report.md"]:
        src = output_dir / filename
        if src.exists():
            shutil.copy2(src, report_dir / filename)
            copied_files.append(filename)
    return copied_files


def register_run(run_id: str, request_path: Path, status: str, started_at: str, finished_at: str) -> None:
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


def main():
    ensure_workspace_structure()
    request_path = get_request_file()
    run_id = os.getenv("RUN_ID") or create_run_id()

    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    report_dir = Path("reports") / run_id
    report_dir.mkdir(parents=True, exist_ok=True)

    request_text = request_path.read_text(encoding="utf-8")

    started_at = datetime.utcnow().isoformat()
    status = "success"

    try:
        result = AlbionFactory().crew().kickoff(
            inputs={"project_goal": request_text}
        )

        copied_files = copy_reports(output_dir, report_dir)

        shutil.copy2(request_path, report_dir / "request.md")
        finished_at = datetime.utcnow().isoformat()

        manifest = {
            "run_id": run_id,
            "request_file": str(request_path).replace("\\", "/"),
            "started_at": started_at,
            "finished_at": finished_at,
            "status": status,
            "copied_reports": copied_files,
            "result_preview": getattr(result, "raw", "")[:1500],
        }
        write_json(report_dir / "manifest.json", manifest)
        register_run(run_id, request_path, status, started_at, finished_at)

        print(getattr(result, "raw", ""))
        print(f"Saved to {report_dir}")

    except Exception as e:
        status = "failed"
        finished_at = datetime.utcnow().isoformat()
        manifest = {
            "run_id": run_id,
            "request_file": str(request_path).replace("\\", "/"),
            "started_at": started_at,
            "finished_at": finished_at,
            "status": status,
            "error": str(e),
        }
        write_json(report_dir / "manifest.json", manifest)
        shutil.copy2(request_path, report_dir / "request.md")
        register_run(run_id, request_path, status, started_at, finished_at)
        raise


if __name__ == "__main__":
    main()