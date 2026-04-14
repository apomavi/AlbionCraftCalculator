"""AODP live price importer skeleton.

Amaç:
- resmi AODP live veri çağrılarını config tabanlı toplamak
- raw response saklamak
- import manifest ve import log üretmek

Not:
- Resmi path dışı endpoint hardcode edilmez.
- prices/history path'leri resmi AODP stats path formatı ile verilir.
- gold endpoint'i config/arg üzerinden açıkça verilmelidir.
"""

from __future__ import annotations

import argparse
import json
import uuid
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

from albion_factory.db import build_postgres_dsn, is_postgres_primary
from albion_factory.log_writer import append_data_change, append_import_run


AODP_BASE_URL = "https://www.albion-online-data.com"
PRICES_PATH = "/api/v2/stats/prices/"
HISTORY_PATH = "/api/v2/stats/history/"


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def build_import_id(prefix: str) -> str:
    return datetime.now(UTC).strftime(f"IMPORT-{prefix}-%Y%m%d-%H%M%S")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_json(url: str) -> str:
    with urlopen(url) as response:  # nosec - controlled skeleton usage
        return response.read().decode("utf-8")


def build_prices_url(item_ids: str, locations: str | None, qualities: str | None) -> str:
    query: dict[str, str] = {}
    if locations:
        query["locations"] = locations
    if qualities:
        query["qualities"] = qualities
    query_string = f"?{urlencode(query)}" if query else ""
    return f"{AODP_BASE_URL}{PRICES_PATH}{item_ids}{query_string}"


def build_history_url(item_ids: str, locations: str | None, time_scale: int | None) -> str:
    query: dict[str, str | int] = {}
    if locations:
        query["locations"] = locations
    if time_scale is not None:
        query["time-scale"] = time_scale
    query_string = f"?{urlencode(query)}" if query else ""
    return f"{AODP_BASE_URL}{HISTORY_PATH}{item_ids}{query_string}"


def persist_live_payload(dataset_name: str, source_url: str, payload_text: str) -> dict:
    import_id = build_import_id(dataset_name.upper())
    started_at = utc_now()
    raw_dir = Path("data/raw") / dataset_name / import_id
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = raw_dir / "payload.json"
    raw_path.write_text(payload_text, encoding="utf-8")
    finished_at = utc_now()

    manifest = {
        "import_id": import_id,
        "dataset_name": dataset_name,
        "source_type": "aodp_live",
        "source_url": source_url,
        "raw_path": str(raw_path).replace("\\", "/"),
        "processed_path": None,
        "db_target": "postgres" if is_postgres_primary() else "sqlite",
        "postgres_dsn": build_postgres_dsn() if is_postgres_primary() else None,
        "status": "raw_collected",
        "notes": "Live importer iskeleti hazır. Normalization ve DB upsert sonraki adımda eklenecek.",
        "started_at": started_at,
        "finished_at": finished_at,
    }
    write_json(Path("data/manifests") / f"{import_id}.json", manifest)

    append_import_run(
        Path("data/logs/import_runs.csv"),
        {
            "import_id": import_id,
            "source_name": source_url,
            "dataset_name": dataset_name,
            "action": "import_live",
            "status": "raw_collected",
            "raw_path": str(raw_path).replace("\\", "/"),
            "processed_path": "",
            "started_at": started_at,
            "finished_at": finished_at,
            "notes": "Normalization henüz uygulanmadı.",
        },
    )
    append_data_change(
        Path("data/logs/data_changes.csv"),
        {
            "change_id": f"CHANGE-{uuid.uuid4().hex[:12]}",
            "dataset_name": dataset_name,
            "change_type": "snapshot_created",
            "record_count": "0",
            "reason": "Live skeleton import initialized",
            "source_run_id": import_id,
            "timestamp": finished_at,
        },
    )
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AODP live price/history/gold importer skeleton")
    parser.add_argument("mode", choices=["prices", "history", "gold"])
    parser.add_argument("--item-ids", help="Virgülle ayrılmış official item id listesi")
    parser.add_argument("--locations", help="Virgülle ayrılmış official location listesi")
    parser.add_argument("--qualities", help="Virgülle ayrılmış quality listesi")
    parser.add_argument("--time-scale", type=int, help="AODP history time-scale değeri")
    parser.add_argument("--gold-url", help="Gold için resmi URL açıkça verilmeli")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.mode == "prices":
        if not args.item_ids:
            raise SystemExit("prices mode için --item-ids gerekli")
        source_url = build_prices_url(args.item_ids, args.locations, args.qualities)
        dataset_name = "market_prices"
    elif args.mode == "history":
        if not args.item_ids:
            raise SystemExit("history mode için --item-ids gerekli")
        source_url = build_history_url(args.item_ids, args.locations, args.time_scale)
        dataset_name = "market_history"
    else:
        if not args.gold_url:
            raise SystemExit("gold mode için --gold-url gerekli")
        source_url = args.gold_url
        dataset_name = "gold_prices"

    payload_text = fetch_json(source_url)
    manifest = persist_live_payload(dataset_name, source_url, payload_text)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()