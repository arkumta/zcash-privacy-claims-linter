# Zcash Privacy Claims Linter

A small, open-source command-line prototype that flags potentially overconfident Zcash privacy statements in documentation and localization files so a human reviewer can check them.

**Important:** This is a heuristic review aid, not a fact checker, legal review, cryptographic analyzer, or authoritative privacy assessment. A finding does not prove that a claim is false. Context matters.

## Current features

- Scans Markdown, MDX, reStructuredText, plain text, HTML, JSON, YAML, TOML, XML, gettext `.po`, and `.strings` files.
- Flags a small initial set of absolute claims about anonymity, universal concealment, metadata, and identity.
- Prints file names, line numbers, excerpts, rationale, suggested action, and a reference link.
- Supports JSON output and non-zero exit status for CI workflows.
- Runs locally and does not upload scanned files.

## Requirements

- Python 3.10+

## Install from a checkout

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\\Scripts\\Activate.ps1
python -m pip install -e ".[dev]"
```

## Usage

```bash
zcash-privacy-lint README.md
zcash-privacy-lint ./docs
zcash-privacy-lint ./docs --format json > privacy-report.json
zcash-privacy-lint ./docs --fail-on-findings
pytest
```

## Initial rules

| Rule | Intent |
|---|---|
| `ZPL001` | Absolute anonymity / untraceability language |
| `ZPL002` | Claims that all transactions or payments are hidden |
| `ZPL003` | Absolute metadata concealment claims |
| `ZPL004` | Absolute claims about real-world identity concealment |

Rules are intentionally conservative starting points and may still produce false positives or miss problematic claims. Do not treat the output as an automatic pass/fail on technical accuracy.

## Privacy and safety

- Files are read locally; the tool makes no network requests.
- Do not add secrets, seed phrases, private keys, viewing keys, or private user data to test fixtures.
- Findings include short text excerpts from scanned files in the output. Review reports before sharing them publicly.
- The tool scans lines independently and does not understand negation, surrounding paragraphs, or technical context.

## Technical references

- [Zcash technology overview](https://z.cash/technology/)
- [Zcash ZIP repository](https://github.com/zcash/zips)
- [ZIP 315: Best Practices for Wallet Implementations](https://github.com/zcash/zips/blob/main/zips/zip-0315.rst)

References are starting points for human review; each rule should eventually cite the narrowest, most relevant technical source.

## Project status

Early prototype. Before use in production, expand the test corpus with maintainer input, measure false positives/negatives, review rule wording, and compare against existing ecosystem tooling.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please propose new rules with examples of both problematic and acceptable wording.

## License

MIT. See [LICENSE](LICENSE).
