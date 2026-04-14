from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Type
from urllib.request import urlopen

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class ReadFileInput(BaseModel):
    path: str = Field(..., description="Repo-relative file path")


class SearchFilesInput(BaseModel):
    path: str = Field(..., description="Directory to search")
    pattern: str = Field(..., description="Regex pattern")
    file_glob: str = Field(default="*", description="Glob pattern")


class FetchUrlInput(BaseModel):
    url: str = Field(..., description="HTTPS URL to fetch")


class FetchToFileInput(BaseModel):
    url: str = Field(..., description="HTTPS URL to fetch")
    output_path: str = Field(..., description="Repo-relative output path")


class RunCommandInput(BaseModel):
    command: str = Field(..., description="Safe local command to execute")


SAFE_COMMAND_PREFIXES = (
    "uv run python",
    "uv run pytest",
    "uv run python -m pytest",
    "python",
    "pytest",
    "git diff",
    "git log",
)

DISALLOWED_SHELL_PATTERNS = (
    "|",
    "&&",
    "||",
    ";",
    " xargs ",
    " sh ",
    " bash ",
)


class ReadRepoFileTool(BaseTool):
    name: str = "read_repo_file"
    description: str = "Reads a repository file and returns text content."
    args_schema: Type[BaseModel] = ReadFileInput

    def _run(self, path: str) -> str:
        return Path(path).read_text(encoding="utf-8")


class SearchRepoFilesTool(BaseTool):
    name: str = "search_repo_files"
    description: str = "Searches files under a directory and returns regex matches with file paths."
    args_schema: Type[BaseModel] = SearchFilesInput

    def _run(self, path: str, pattern: str, file_glob: str = "*") -> str:
        root = self._normalize_root(path)
        file_glob = self._normalize_glob(file_glob)
        regex = re.compile(pattern)
        matches: list[dict[str, str]] = []
        scanned_files = 0
        max_files = 400
        max_matches = 40
        skipped_large_files = 0
        for file_path in root.rglob(file_glob):
            if not file_path.is_file():
                continue
            if self._should_skip_path(file_path):
                continue
            scanned_files += 1
            if scanned_files > max_files:
                break
            try:
                if file_path.stat().st_size > 512_000:
                    skipped_large_files += 1
                    continue
                text = file_path.read_text(encoding="utf-8")
            except Exception:
                continue
            if regex.search(text):
                matches.append(
                    {
                        "path": str(file_path).replace("\\", "/"),
                        "preview": text[:220].replace("\n", " ").strip(),
                    }
                )
                if len(matches) >= max_matches:
                    break
        return json.dumps(
            {
                "root": str(root).replace("\\", "/"),
                "file_glob": file_glob,
                "scanned_files": scanned_files,
                "skipped_large_files": skipped_large_files,
                "matches": matches,
                "truncated": scanned_files > max_files or len(matches) >= max_matches,
            },
            ensure_ascii=False,
        )

    def _normalize_root(self, path: str) -> Path:
        candidate = path.strip().replace("\\", "/")
        workspace_root = Path.cwd()

        if candidate in {"", ".", "/", "./", "\\"}:
            return workspace_root

        normalized = Path(candidate)
        if normalized.is_absolute():
            try:
                normalized = normalized.relative_to(normalized.anchor)
            except Exception:
                return workspace_root

        resolved = (workspace_root / normalized).resolve()
        try:
            resolved.relative_to(workspace_root.resolve())
        except Exception:
            return workspace_root

        if not resolved.exists():
            return workspace_root
        return resolved

    def _normalize_glob(self, file_glob: str) -> str:
        normalized = file_glob.strip() or "*"
        if normalized in {"**", "**/*", "*.*"}:
            return "*"
        return normalized

    def _should_skip_path(self, path: Path) -> bool:
        parts = {part.lower() for part in path.parts}
        noisy_dirs = {".git", ".venv", "node_modules", "__pycache__", "externals", "bin"}
        return bool(parts & noisy_dirs)


class FetchUrlTool(BaseTool):
    name: str = "fetch_url"
    description: str = "Fetches a HTTPS URL and returns text content."
    args_schema: Type[BaseModel] = FetchUrlInput

    def _run(self, url: str) -> str:
        if not url.startswith("https://"):
            raise ValueError("Only https:// URLs are allowed")
        with urlopen(url) as response:  # nosec - constrained by https allow rule
            return response.read().decode("utf-8", errors="ignore")[:20000]


class FetchUrlToFileTool(BaseTool):
    name: str = "fetch_url_to_file"
    description: str = "Fetches a HTTPS URL and saves it to a repo-relative file path."
    args_schema: Type[BaseModel] = FetchToFileInput

    def _run(self, url: str, output_path: str) -> str:
        if not url.startswith("https://"):
            raise ValueError("Only https:// URLs are allowed")
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with urlopen(url) as response:  # nosec - constrained by https allow rule
            body = response.read().decode("utf-8", errors="ignore")
        target.write_text(body, encoding="utf-8")
        return f"saved:{str(target).replace('\\', '/')}"


class RunSafeCommandTool(BaseTool):
    name: str = "run_safe_command"
    description: str = "Runs a safe local command. ALLOWED PREFIXES ONLY: python, pytest, git. DO NOT USE 'echo', 'cat', or shell pipelines."
    args_schema: Type[BaseModel] = RunCommandInput

    def _run(self, command: str) -> str:
        if not command.startswith(SAFE_COMMAND_PREFIXES):
            raise ValueError("Command not in allowed safe prefixes")
        lowered = f" {command.lower()} "
        if any(token in lowered for token in DISALLOWED_SHELL_PATTERNS):
            raise ValueError("Command contains disallowed shell chaining or unsafe patterns")
        completed = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return json.dumps(
            {
                "returncode": completed.returncode,
                "stdout": completed.stdout[-4000:],
                "stderr": completed.stderr[-4000:],
            },
            ensure_ascii=False,
        )