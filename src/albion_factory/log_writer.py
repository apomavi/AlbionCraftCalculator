from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


IMPORT_RUN_HEADERS = [
    "import_id",
    "source_name",
    "dataset_name",
    "action",
    "status",
    "raw_path",
    "processed_path",
    "started_at",
    "finished_at",
    "notes",
]

DATA_CHANGE_HEADERS = [
    "change_id",
    "dataset_name",
    "change_type",
    "record_count",
    "reason",
    "source_run_id",
    "timestamp",
]


def _normalize_csv_file(csv_path: Path, headers: Iterable[str]) -> None:
    if not csv_path.exists() or csv_path.stat().st_size == 0:
        return

    header_line = ",".join(headers)
    content = csv_path.read_text(encoding="utf-8")
    normalized = content.replace("\r\n", "\n").replace("\r", "\n")

    if normalized.startswith(header_line) and normalized != header_line:
        remainder = normalized[len(header_line):]
        if remainder and not remainder.startswith("\n"):
            normalized = f"{header_line}\n{remainder}"

    if normalized and not normalized.endswith("\n"):
        normalized = f"{normalized}\n"

    if normalized != content:
        csv_path.write_text(normalized, encoding="utf-8", newline="\n")


def append_csv_row(csv_path: Path, headers: list[str], row: dict[str, str]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    _normalize_csv_file(csv_path, headers)
    exists = csv_path.exists() and csv_path.stat().st_size > 0
    with csv_path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def append_import_run(csv_path: Path, row: dict[str, str]) -> None:
    append_csv_row(csv_path, IMPORT_RUN_HEADERS, row)


def append_data_change(csv_path: Path, row: dict[str, str]) -> None:
    append_csv_row(csv_path, DATA_CHANGE_HEADERS, row)