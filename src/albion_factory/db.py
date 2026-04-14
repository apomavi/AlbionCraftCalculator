from __future__ import annotations

import os
import sqlite3
from pathlib import Path


def get_env(name: str, default: str) -> str:
    return os.getenv(name, default)


def get_schema_path() -> Path:
    return Path(get_env("SCHEMA_FILE", "sql/001_create_core_tables.sql"))


def get_sqlite_path() -> Path:
    return Path(get_env("SQLITE_PATH", "data/test_schema.db"))


def is_postgres_primary() -> bool:
    return get_env("DB_TARGET", "postgres").lower() == "postgres"


def build_postgres_dsn() -> str:
    host = get_env("POSTGRES_HOST", "localhost")
    port = get_env("POSTGRES_PORT", "5432")
    db = get_env("POSTGRES_DB", "albion_factory")
    user = get_env("POSTGRES_USER", "postgres")
    password = get_env("POSTGRES_PASSWORD", "postgres")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


def apply_schema_sqlite(sql_path: Path | None = None, sqlite_path: Path | None = None) -> Path:
    schema_path = sql_path or get_schema_path()
    db_path = sqlite_path or get_sqlite_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    sql = schema_path.read_text(encoding="utf-8")

    with sqlite3.connect(db_path) as connection:
        connection.executescript(sql)
        connection.commit()

    return db_path


def apply_schema_postgres(sql_path: Path | None = None) -> str:
    schema_path = sql_path or get_schema_path()
    sql = schema_path.read_text(encoding="utf-8")

    try:
        import psycopg
    except ImportError as exc:
        raise RuntimeError(
            "psycopg is not installed. Run 'uv sync' before applying PostgreSQL schema."
        ) from exc

    dsn = build_postgres_dsn()
    with psycopg.connect(dsn) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
    return dsn


def apply_schema(target: str = "postgres") -> str:
    if target == "sqlite":
        return str(apply_schema_sqlite())
    if target == "postgres":
        return apply_schema_postgres()
    raise ValueError("target must be 'postgres' or 'sqlite'")


if __name__ == "__main__":
    target = os.getenv("DB_TARGET", "postgres")
    result = apply_schema(target)
    print(result)