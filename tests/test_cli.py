import json
from pathlib import Path
from zcash_privacy_lint.cli import main

def test_json_report(tmp_path: Path, monkeypatch, capsys):
    file = tmp_path / "README.md"
    file.write_text("Your transactions are untraceable.\n", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["zcash-privacy-lint", str(file), "--format", "json"])
    try:
        main()
    except SystemExit as exc:
        assert exc.code in (None, 0)
    payload = json.loads(capsys.readouterr().out)
    assert payload["finding_count"] >= 1
    assert payload["findings"][0]["path"] == "README.md"
