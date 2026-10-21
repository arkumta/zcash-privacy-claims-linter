
from zcash_privacy_lint.scanner import scan_text


def test_flags_absolute_anonymity_claim():
    findings = scan_text(
        "Our wallet makes every payment completely anonymous.", "README.md"
    )
    assert any(f.rule_id == "ZPL001" for f in findings)


def test_flags_metadata_claim():
    findings = scan_text("No metadata is exposed.", "docs/privacy.md")
    assert any(f.rule_id == "ZPL003" for f in findings)


def test_does_not_flag_qualified_statement():
    text = (
        "Shielded transactions protect selected details "
        "from ordinary public observers."
    )
    assert scan_text(text, "docs/privacy.md") == []


def test_finding_has_line_number_and_reference():
    findings = scan_text(
        "First line\nYour funds are 100% anonymous.", "README.md"
    )
    assert len(findings) == 1
    assert findings[0].line == 2
    assert findings[0].reference_url.startswith("https://")


def test_flags_untraceable_claim():
    findings = scan_text("Payments are fully untraceable.", "README.md")
    assert any(f.rule_id == "ZPL001" for f in findings)


def test_flags_absolute_tracking_claim():
    findings = scan_text("It is impossible to track transactions.", "README.md")
    assert any(f.rule_id == "ZPL005" for f in findings)


def test_flags_universal_concealment_claim():
    findings = scan_text("Every payment is shielded.", "README.md")
    assert any(f.rule_id == "ZPL002" for f in findings)


def test_qualified_privacy_statement_is_not_flagged():
    text = (
        "Shielded transactions can protect selected transaction details, "
        "but protection depends on how the funds are used."
    )
    assert scan_text(text, "README.md") == []


def test_finding_preserves_file_line():
    findings = scan_text(
        "Introduction\nPrivacy details\nNo metadata is exposed.",
        "docs/guide.md",
    )
    match = next(f for f in findings if f.rule_id == "ZPL003")
    assert match.path == "docs/guide.md"
    assert match.line == 3

def test_does_not_flag_explicit_criticism_of_a_claim():
    text = (
        "The claim that every payment is completely anonymous is misleading."
    )
    assert scan_text(text, "docs/review.md") == []


def test_still_flags_a_direct_absolute_claim():
    text = "Every payment is completely anonymous."
    findings = scan_text(text, "docs/marketing.md")
    assert any(f.rule_id == "ZPL001" for f in findings)
