#!/usr/bin/env python3
"""Validate the structural invariants of the dissertation writing memory."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


ALLOWED_STATUSES = {
    "Погоджено",
    "Уникати",
    "Контекстне",
    "Очікує рішення",
    "Замінено",
}


def is_modified_in_git(root: Path, path: Path) -> bool:
    try:
        relative = path.resolve().relative_to(root.resolve())
    except ValueError:
        return False

    result = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain", "--", str(relative)],
        check=False,
        capture_output=True,
        text=True,
    )
    return bool(result.stdout.strip())


def validate(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    readme_path = root / "memory" / "README.md"
    memory_path = root / "memory" / "MEMORY.md"

    for path in (readme_path, memory_path):
        if not path.is_file():
            errors.append(f"Missing required file: {path}")

    if errors:
        return errors, warnings

    text = memory_path.read_text(encoding="utf-8")

    portable_files = (
        readme_path,
        memory_path,
        root / "AGENTS.md",
        root / ".agents" / "skills" / "dissertation-memory" / "SKILL.md",
        root / ".codex" / "agents" / "memory-auditor.toml",
    )
    for portable_path in portable_files:
        if not portable_path.is_file():
            continue
        portable_text = portable_path.read_text(encoding="utf-8")
        if re.search(r"[A-Za-z]:\\", portable_text):
            errors.append(f"Absolute Windows path found in portable file: {portable_path}")

    if "my/dissertation_writing_memory" in text:
        errors.append("MEMORY.md still references the obsolete memory path")

    statuses = re.findall(r"\*\*Статус:\*\*\s*`([^`]+)`", text)
    for status in statuses:
        if status not in ALLOWED_STATUSES:
            errors.append(f"Unsupported status: {status}")

    ids = re.findall(r"^###\s+(MEM-[A-Z]+-[^\s]+)", text, flags=re.MULTILINE)
    concrete_ids = [item for item in ids if "YYYY" not in item and "NNN" not in item]
    duplicates = sorted({item for item in concrete_ids if concrete_ids.count(item) > 1})
    for item in duplicates:
        errors.append(f"Duplicate memory id: {item}")

    pending_sections = re.split(r"(?=^###\s+MEM-)", text, flags=re.MULTILINE)
    for section in pending_sections:
        if "**Статус:** `Очікує рішення`" not in section:
            continue
        heading = re.search(r"^###\s+([^\n]+)", section, flags=re.MULTILINE)
        if heading and "YYYY" not in heading.group(1) and "**Рішення автора:**" not in section:
            errors.append(f"Pending record lacks an author-decision field: {heading.group(1)}")

        if not heading or "YYYY" in heading.group(1):
            continue

        required_fields = (
            "**Місце:**",
            "**Що визнано правильним:**",
            "**Що потребує виправлення:**",
            "**Рішення автора:**",
        )
        for field in required_fields:
            if field not in section:
                errors.append(f"Pending record lacks {field} {heading.group(1)}")

        location = re.search(r"\*\*Місце:\*\*\s*`([^`]+)`", section)
        if location:
            raw_path = location.group(1).split(",", maxsplit=1)[0].strip()
            manuscript_path = Path(raw_path)
            if not manuscript_path.is_absolute():
                manuscript_path = root / manuscript_path
            if manuscript_path.is_file() and is_modified_in_git(root, manuscript_path):
                record_id = heading.group(1).split("—", maxsplit=1)[0].strip()
                relative_path = manuscript_path.resolve().relative_to(root.resolve()).as_posix()
                warnings.append(
                    "Pending record points to a modified worktree file; confirm author approval: "
                    f"{record_id} -> {relative_path}"
                )

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    errors, warnings = validate(root)

    for warning in warnings:
        print(f"WARNING: {warning}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"Memory validation passed with {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
