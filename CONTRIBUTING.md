# Contributing

Thanks for helping improve the Zcash Privacy Claims Linter.

## Before proposing a rule

Please include:
1. The exact statement or a clearly labeled synthetic example.
2. Why it could mislead readers about Zcash privacy.
3. A supporting authoritative source.
4. At least one false-positive example that should not be flagged.
5. A test demonstrating expected behavior.

## Development

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Guidelines

- Findings are review prompts, not automatic truth judgments.
- Prefer precise, source-backed rules over broad keyword lists.
- Never include secrets, private keys, seed phrases, viewing keys, or private user data in fixtures.
- Keep scanned content local; do not add telemetry or network uploads without explicit design review.
- Explain uncertainty and known limitations in rule messages.

## Pull requests

Describe the user problem, evidence for the rule, expected false positives, tests, and any documentation changes.
