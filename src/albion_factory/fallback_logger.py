from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _enabled() -> bool:
    return os.getenv("FALLBACK_DEBUG", "1").strip().lower() not in {"0", "false", "no"}


def log_fallback_event(kind: str, message: str, **extra: Any) -> None:
    if not _enabled():
        return

    event = {
        "ts": datetime.now(UTC).isoformat(),
        "kind": kind,
        "message": message,
        **extra,
    }

    print(f"[{kind}] {message}")

    log_path_raw = os.getenv("FALLBACK_EVENT_LOG", "")
    if not log_path_raw:
        return

    log_path = Path(log_path_raw)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")