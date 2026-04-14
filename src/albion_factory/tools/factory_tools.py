from __future__ import annotations

import csv
from pathlib import Path
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class ReadFileInput(BaseModel):
    path: str = Field(..., description="Repo-relative file path")


class NormalizeCsvInput(BaseModel):
    path: str = Field(..., description="Repo-relative CSV path")


class InspectFileInput(BaseModel):
    path: str = Field(..., description="Repo-relative file path")


class VerifyCsvInput(BaseModel):
    path: str = Field(..., description="Repo-relative CSV path")


class VerifyTextStructureInput(BaseModel):
    path: str = Field(..., description="Repo-relative text/code file path")
    required_terms: list[str] = Field(default_factory=list, description="Terms expected in file content")


class WriteRepoFileInput(BaseModel):
    path: str = Field(..., description="Repo-relative text/code file path")
    content: str = Field(..., description="Full file content to write")


class ReadRepoFileTool(BaseTool):
    name: str = "read_repo_file"
    description: str = "Reads a repository text file and returns its content."
    args_schema: Type[BaseModel] = ReadFileInput

    def _run(self, path: str) -> str:
        file_path = Path(path)
        return file_path.read_text(encoding="utf-8")


class NormalizeCsvNewlinesTool(BaseTool):
    name: str = "normalize_csv_newlines"
    description: str = "Repairs merged CSV header/row newline issues in-place for a target file."
    args_schema: Type[BaseModel] = NormalizeCsvInput

    def _run(self, path: str) -> str:
        csv_path = Path(path)
        content = csv_path.read_text(encoding="utf-8")
        original_lines = len(content.splitlines())
        normalized = content.replace("\r\n", "\n").replace("\r", "\n")

        header = "import_id,source_name,dataset_name,action,status,raw_path,processed_path,started_at,finished_at,notes"
        if normalized.startswith(header) and normalized != header:
            remainder = normalized[len(header):]
            if remainder and not remainder.startswith("\n"):
                normalized = f"{header}\n{remainder}"

        if normalized and not normalized.endswith("\n"):
            normalized = f"{normalized}\n"

        csv_path.write_text(normalized, encoding="utf-8", newline="\n")
        normalized_lines = len(normalized.splitlines())
        return (
            f"Action: normalized_csv_newlines\n"
            f"Target File: {path}\n"
            f"Original Line Count: {original_lines}\n"
            f"Normalized Line Count: {normalized_lines}\n"
            f"Result: CSV newline normalization applied successfully"
        )


class InspectRepoFileTool(BaseTool):
    name: str = "inspect_repo_file"
    description: str = "Reads a repository file and returns a short structured inspection summary."
    args_schema: Type[BaseModel] = InspectFileInput

    def _run(self, path: str) -> str:
        file_path = Path(path)
        text = file_path.read_text(encoding="utf-8")
        lines = text.splitlines()
        preview = "\n".join(lines[:8])
        return (
            f"Target File: {path}\n"
            f"Line Count: {len(lines)}\n"
            f"Character Count: {len(text)}\n"
            f"Preview:\n{preview}"
        )


class VerifyCsvStructureTool(BaseTool):
    name: str = "verify_csv_structure"
    description: str = "Checks whether a CSV file is parsable and header is separated from rows."
    args_schema: Type[BaseModel] = VerifyCsvInput

    def _run(self, path: str) -> str:
        csv_path = Path(path)
        content = csv_path.read_text(encoding="utf-8")
        lines = [line for line in content.splitlines() if line.strip()]
        if len(lines) < 2:
            return "FAIL: CSV has fewer than 2 non-empty lines"

        try:
            with csv_path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.reader(handle))
        except Exception as exc:
            return f"FAIL: CSV parse error: {exc}"

        if len(rows) < 2:
            return "FAIL: CSV parser did not detect data rows"

        header = rows[0]
        first_row = rows[1]
        if len(header) != len(first_row):
            return "FAIL: Header/data column count mismatch"

        return f"PASS: CSV structure is valid with {len(rows) - 1} data rows"


class VerifyTextStructureTool(BaseTool):
    name: str = "verify_text_structure"
    description: str = "Checks whether a text/code file exists, is readable, and contains required terms."
    args_schema: Type[BaseModel] = VerifyTextStructureInput

    def _run(self, path: str, required_terms: list[str] | None = None) -> str:
        file_path = Path(path)
        if not file_path.exists():
            return f"FAIL: File not found: {path}"

        text = file_path.read_text(encoding="utf-8")
        required_terms = required_terms or []
        missing = [term for term in required_terms if term not in text]
        if missing:
            return f"FAIL: Missing required terms: {missing}"

        return f"PASS: Text structure is valid for {path}"


class WriteRepoFileTool(BaseTool):
    name: str = "write_repo_file"
    description: str = "Creates or overwrites a repository text/code file with provided content. Use only for intentional implementation changes."
    args_schema: Type[BaseModel] = WriteRepoFileInput

    def _run(self, path: str, content: str) -> str:
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return f"PASS: Wrote file {path} with {len(content.splitlines())} lines"