import csv
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Iterable


REQUEST_PATTERN = re.compile(r"REQ-(\d{4})\.md$")


def ensure_workspace_structure() -> None:
    for relative_path in [
        "requests",
        "reports",
        "decisions",
        "data/raw",
        "data/processed",
        "data/manifests",
        "data/logs",
        "runs",
        "output",
    ]:
        Path(relative_path).mkdir(parents=True, exist_ok=True)


def resolve_request_file(request_file: str | None = None) -> Path:
    requests_dir = Path("requests")
    if request_file:
        path = Path(request_file)
        if not path.exists():
            raise FileNotFoundError(f"Request file not found: {path}")
        if path.parent != requests_dir or not REQUEST_PATTERN.match(path.name):
            raise RuntimeError(
                "Deprecated request path. Ana giriş sadece requests/REQ-xxxx.md olmalı."
            )
        return path

    candidates = sorted(
        [path for path in requests_dir.glob("REQ-*.md") if REQUEST_PATTERN.match(path.name)]
    )
    if not candidates:
        raise FileNotFoundError("requests/ altında REQ-xxxx.md formatında request bulunamadı.")
    return candidates[-1]


def create_run_id(now: datetime | None = None) -> str:
    timestamp = (now or datetime.now()).strftime("RUN-%Y%m%d-%H%M%S")
    report_root = Path("reports")
    candidate = timestamp
    counter = 1
    while (report_root / candidate).exists():
        candidate = f"{timestamp}-{counter:02d}"
        counter += 1
    return candidate


def append_csv_row(csv_path: Path, headers: Iterable[str], row: dict[str, str]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = csv_path.exists()
    with csv_path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(headers))
        if not file_exists or csv_path.stat().st_size == 0:
            writer.writeheader()
        writer.writerow(row)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")