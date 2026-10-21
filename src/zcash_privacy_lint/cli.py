
"""Command-line interface."""
import argparse
import json
import sys
from pathlib import Path
from urllib.parse import quote

from . import __version__
from .scanner import scan_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="zcash-privacy-lint",
        description=(
            "Flag potentially overconfident Zcash privacy claims for human "
            "review. This heuristic tool does not decide whether claims "
            "are true or false."
        ),
    )
    parser.add_argument("path", help="File or directory to scan")
    parser.add_argument(
        "--format",
        choices=("text", "json", "github"),
        default="text",
        help="Output format (default: text; github emits Actions annotations)",
    )
    parser.add_argument(
        "--fail-on-findings",
        action="store_true",
        help="Exit with status 1 when findings are reported (useful in CI).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def _github_escape(value: str) -> str:
    """Escape data values for GitHub Actions workflow commands."""
    return (
        value.replace("%", "%25")
        .replace("\r", "%0D")
        .replace("\n", "%0A")
        .replace(":", "%3A")
        .replace(",", "%2C")
    )


def _github_property(value: str) -> str:
    """Escape a property value in a GitHub Actions annotation."""
    return (
        value.replace("%", "%25")
        .replace("\r", "%0D")
        .replace("\n", "%0A")
        .replace(":", "%3A")
        .replace(",", "%2C")
    )


def main() -> None:
    args = build_parser().parse_args()
    target = Path(args.path)

    if not target.exists():
        print(f"error: path does not exist: {target}", file=sys.stderr)
        raise SystemExit(2)

    if not target.is_file() and not target.is_dir():
        print(f"error: not a regular file or directory: {target}", file=sys.stderr)
        raise SystemExit(2)

    findings = scan_path(target)

    if args.format == "json":
        report = {
            "tool": "zcash-privacy-claims-linter",
            "version": __version__,
            "target": str(target),
            "finding_count": len(findings),
            "findings": [finding.to_dict() for finding in findings],
            "disclaimer": (
                "Findings are heuristic review prompts, not determinations "
                "that a statement is false or technically incorrect."
            ),
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))

    elif args.format == "github":
        for finding in findings:
            file_path = _github_property(finding.path)
            title = _github_property(
                f"{finding.rule_id} {finding.title}"
            )
            message = _github_escape(
                f"{finding.rationale} Suggested action: "
                f"{finding.recommendation} Reference: {finding.reference_url}"
            )
            print(
                f"::warning file={file_path},line={finding.line},"
                f"title={title}::{message}"
            )

        print(
            f"Zcash Privacy Claims Linter {__version__}: "
            f"{len(findings)} review finding(s).",
            file=sys.stderr,
        )

    else:
        print(
            f"Zcash Privacy Claims Linter {__version__}\n"
            f"Target: {target}\n"
            f"Findings: {len(findings)}\n"
            + "-" * 72
        )
        for finding in findings:
            print(
                f"{finding.path}:{finding.line}: "
                f"[{finding.rule_id}] {finding.title}\n"
                f"  Text: {finding.excerpt}\n"
                f"  Why review: {finding.rationale}\n"
                f"  Suggested action: {finding.recommendation}\n"
                f"  Reference: {finding.reference_url}\n"
            )
        print(
            "Note: findings are prompts for human review, not proof of inaccuracy."
        )

    if args.fail_on_findings and findings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
