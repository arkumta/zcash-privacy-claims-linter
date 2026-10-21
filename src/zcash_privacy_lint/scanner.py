
"""File scanning and finding generation."""

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .rules import RULES, Rule


SUPPORTED_EXTENSIONS = {
    ".md", ".mdx", ".rst", ".txt", ".html", ".htm",
    ".json", ".yaml", ".yml", ".toml", ".xml", ".po", ".strings",
}

IGNORED_DIRS = {
    ".git", ".venv", "venv", "node_modules", "dist",
    "build", "__pycache__", ".pytest_cache",
}


@dataclass(frozen=True)
class Finding:
    rule_id: str
    title: str
    severity: str
    path: str
    line: int
    excerpt: str
    rationale: str
    recommendation: str
    reference_url: str

    def to_dict(self) -> dict:
        return asdict(self)


def iter_files(target: Path) -> Iterable[Path]:
    """Yield supported files from a file or directory."""
    if target.is_file():
        if target.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield target
        return

    for path in sorted(target.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        if any(part in IGNORED_DIRS for part in path.parts):
            continue

        try:
            if path.stat().st_size > 1_000_000:
                continue
        except OSError:
            continue

        yield path


def scan_text(
    text: str,
    path: str = "<text>",
    rules: tuple[Rule, ...] = RULES,
) -> list[Finding]:
    """Scan text for potentially overconfident privacy claims.

    Explicit critical-discussion phrases are skipped to reduce some
    false positives. This is heuristic filtering, not full language analysis.
    """
    findings: list[Finding] = []

    critical_discussion = re.compile(
        r"\b(?:the claim that|this claim that|the statement that|"
        r"this statement that|the phrase|the wording|"
        r"is misleading|is inaccurate|is an overstatement|"
        r"should not claim|shouldn't claim)\b",
        re.I,
    )

    for line_number, line in enumerate(text.splitlines(), start=1):
        # Conservative heuristic: skip lines explicitly framed as criticism.
        if critical_discussion.search(line):
            continue

        for rule in rules:
            if rule.pattern.search(line):
                excerpt = line.strip()
                if len(excerpt) > 240:
                    excerpt = excerpt[:237] + "..."

                findings.append(
                    Finding(
                        rule.id,
                        rule.title,
                        "review",
                        path,
                        line_number,
                        excerpt,
                        rule.rationale,
                        rule.recommendation,
                        rule.reference_url,
                    )
                )

    return findings


def scan_path(
    target: Path,
    rules: tuple[Rule, ...] = RULES,
) -> list[Finding]:
    """Scan a supported file or recursively scan a directory."""
    findings: list[Finding] = []

    for file_path in iter_files(target):
        try:
            text = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        try:
            base_path = target if target.is_dir() else target.parent
            display_path = str(file_path.relative_to(base_path))
        except ValueError:
            display_path = str(file_path)

        findings.extend(scan_text(text, display_path, rules))

    return findings
