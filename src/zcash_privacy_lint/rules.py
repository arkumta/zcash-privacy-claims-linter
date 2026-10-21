
"""Heuristic privacy-claim rules; findings require human review."""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Rule:
    id: str
    title: str
    pattern: re.Pattern[str]
    rationale: str
    recommendation: str
    reference_url: str


REFERENCE = "https://z.cash/technology/"

RULES: tuple[Rule, ...] = (
    Rule(
        "ZPL001",
        "Absolute anonymity claim",
        re.compile(
            r"\b(?:100\s*%\s*anonymous|completely anonymous|totally anonymous|"
            r"fully anonymous|untraceable|impossible to trace|cannot be traced|"
            r"can't be traced|fully untraceable)\b",
            re.I,
        ),
        "Absolute language can overstate privacy guarantees. Privacy depends on "
        "transaction type, wallet behavior, information disclosed elsewhere, "
        "and what an observer already knows.",
        "Describe the specific protection and its limits. Avoid absolute "
        "guarantees unless carefully qualified and technically substantiated.",
        REFERENCE,
    ),
    Rule(
        "ZPL002",
        "Universal concealment claim",
        re.compile(
            r"\b(?:all|every)\s+(?:transactions?|payments?|transfers?)\s+"
            r"(?:are|is)\s+(?:private|hidden|shielded)\b|"
            r"\b(?:always hides|hides all)\s+(?:transaction|payment|transfer)\s+"
            r"(?:details|information|metadata)\b",
            re.I,
        ),
        "Zcash supports transparent and shielded transaction flows. A claim "
        "covering every transaction or field may omit important distinctions.",
        "Specify the transaction type and fields protected, and explain that "
        "visibility depends on the transaction path.",
        REFERENCE,
    ),
    Rule(
        "ZPL003",
        "Absolute metadata protection claim",
        re.compile(
            r"\b(?:no metadata is exposed|zero metadata exposure|"
            r"all metadata is hidden|metadata is never visible|"
            r"no metadata can be seen|metadata is completely protected)\b",
            re.I,
        ),
        "Even when shielded transaction details are protected, other activity "
        "or external context may reveal information.",
        "Name the metadata in question and distinguish on-chain fields from "
        "information that may be inferred or disclosed elsewhere.",
        REFERENCE,
    ),
    Rule(
        "ZPL004",
        "Absolute identity concealment claim",
        re.compile(
            r"\b(?:nobody can know who you are|no one can know who you are|"
            r"your identity is impossible to discover|"
            r"guaranteed identity protection|identity is always hidden|"
            r"your identity can never be discovered)\b",
            re.I,
        ),
        "Shielded transaction properties do not guarantee that a user's "
        "real-world identity cannot be inferred from other information.",
        "Explain what the protocol protects and avoid guarantees about "
        "real-world identity or activity outside the blockchain.",
        REFERENCE,
    ),
    Rule(
        "ZPL005",
        "Absolute tracking-prevention claim",
        re.compile(
            r"\b(?:impossible to track|cannot be tracked|can't be tracked|"
            r"nobody can track you|no one can track you|"
            r"completely untrackable|tracking is impossible)\b",
            re.I,
        ),
        "Absolute tracking claims may overlook information outside the "
        "protected transaction data, including disclosures and observer context.",
        "Describe what an observer can and cannot learn, and qualify the claim "
        "by transaction type and threat model.",
        REFERENCE,
    ),
)
