"""Static Albion data importer skeleton.

Amaç:
- item ve location gibi statik verileri import etmek
- raw/manifests/logs append-only zincirine bağlanmak
- gerçek veri kaynağını config ile seçilebilir bırakmak
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import UTC, datetime
from pathlib import Path


DATASET_NAME = "items_static"


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def build_import_id() -> str:
    return datetime.now(UTC).strftime("IMPORT-ITEMS-%Y%m%d-%H%M%S")


def append_csv_row(csv_path: Path, headers: list[str], row: dict[str, str]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    exists = csv_path.exists() and csv_path.stat().st_size > 0
    with csv_path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def run_import(source_path: Path, dataset_name: str = DATASET_NAME) -> dict:
    import_id = build_import_id()
    started_at = utc_now()
    raw_dir = Path("data/raw") / dataset_name / import_id
    manifest_path = Path("data/manifests") / f"{import_id}.json"
    raw_dir.mkdir(parents=True, exist_ok=True)

    copied_source = raw_dir / source_path.name
    copied_source.write_bytes(source_path.read_bytes())

    finished_at = utc_now()
    manifest = {
        "import_id": import_id,
        "dataset_name": dataset_name,
        "source_type": "static_file",
        "source_path": str(source_path).replace("\\", "/"),
        "raw_path": str(copied_source).replace("\\", "/"),
        "processed_path": None,
        "status": "skeleton_only",
        "notes": "Static importer iskeleti hazır. DB upsert katmanı sonraki adımda eklenecek.",
        "started_at": started_at,
        "finished_at": finished_at,
    }
    write_json(manifest_path, manifest)

    append_csv_row(
        Path("data/logs/import_runs.csv"),
        [
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
        ],
        {
            "import_id": import_id,
            "source_name": source_path.name,
            "dataset_name": dataset_name,
            "action": "import_static",
            "status": "skeleton_only",
            "raw_path": str(copied_source).replace("\\", "/"),
            "processed_path": "",
            "started_at": started_at,
            "finished_at": finished_at,
            "notes": "DB import iskeleti henüz uygulanmadı.",
        },
    )
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Static item/location importer skeleton")
    parser.add_argument("--source", required=True, help="Static kaynak dosya yolu")
    parser.add_argument("--dataset", default=DATASET_NAME, help="Dataset adı")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest = run_import(Path(args.source), args.dataset)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()