import json
import os
import shutil
from datetime import datetime
from pathlib import Path

from albion_factory.crew import AlbionFactory


def get_request_file() -> Path:
    request_file = os.getenv("REQUEST_FILE")
    if not request_file:
        raise RuntimeError("REQUEST_FILE environment variable is missing.")
    path = Path(request_file)
    if not path.exists():
        raise FileNotFoundError(f"Request file not found: {path}")
    return path


def main():
    request_path = get_request_file()
    run_id = os.getenv("RUN_ID", datetime.now().strftime("RUN-%Y%m%d-%H%M%S"))

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

        for filename in ["lead_report.md", "research_report.md", "validator_report.md"]:
            src = output_dir / filename
            if src.exists():
                shutil.copy2(src, report_dir / filename)

        shutil.copy2(request_path, report_dir / "request.md")

        manifest = {
            "run_id": run_id,
            "request_file": str(request_path),
            "started_at": started_at,
            "finished_at": datetime.utcnow().isoformat(),
            "status": status,
            "result_preview": getattr(result, "raw", "")[:1500],
        }
        (report_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        print(getattr(result, "raw", ""))
        print(f"Saved to {report_dir}")

    except Exception as e:
        status = "failed"
        manifest = {
            "run_id": run_id,
            "request_file": str(request_path),
            "started_at": started_at,
            "finished_at": datetime.utcnow().isoformat(),
            "status": status,
            "error": str(e),
        }
        (report_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        shutil.copy2(request_path, report_dir / "request.md")
        raise


if __name__ == "__main__":
    main()