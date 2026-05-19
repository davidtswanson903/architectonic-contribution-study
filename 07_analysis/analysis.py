from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = ROOT / "02_sampling" / "journal_sample.csv"
POLICY_PATH = ROOT / "04_journal_policy_coding" / "policy_coding.csv"
ARTICLE_PATH = ROOT / "06_article_coding" / "article_contribution_coding.csv"
RESULTS_PATH = Path(__file__).with_name("results_summary.md")
TABLES_DIR = Path(__file__).with_name("tables")

POLICY_CODE_FIELDS = [
    "language_status",
    "activity_status",
    "peer_review_status",
    "research_article_status",
    "inclusion_status",
    "documentation_availability",
    "documentation_orientation",
    "review_process_transparency",
    "reviewer_criteria_visibility",
    "desk_review_transparency",
    "originality_language",
    "literature_grounding_language",
    "debate_entry_language",
    "general_interest_language",
    "specialist_legibility_language",
    "philosophical_content_language",
    "anti_expository_language",
    "argument_centrality_language",
    "synthesis_recognition",
    "field_mapping_recognition",
    "framework_recognition",
    "methodological_recognition",
    "interdisciplinary_recognition",
    "architectonic_vocabulary",
    "scope_openness",
    "formal_openness_to_nonstandard_work",
    "reviewer_criteria_opacity",
    "contribution_criteria_opacity",
    "article_type_opacity",
    "desk_review_opacity",
    "nonstandard_work_opacity",
    "scope_opacity",
    "decision_process_opacity",
    "policy_opacity_level",
    "journal_reviewability_profile",
]

ARTICLE_CONFIDENCE_INCLUDED = {"medium", "high"}
ARCHITECTONIC_PRIMARY_TYPES = {"architectonic", "architectonic_object", "operational_formalizing"}


def read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def summarize_sample(sample_rows: list[dict]) -> list[dict]:
    counts = Counter(
        row.get("primary_category", "")
        for row in sample_rows
        if row.get("sample_id") or row.get("journal_id") or row.get("journal_name")
    )
    return [
        {"primary_category": category, "journal_count": count}
        for category, count in sorted(counts.items())
    ]


def summarize_policy(policy_rows: list[dict]) -> list[dict]:
    summary: list[dict] = []
    for field in POLICY_CODE_FIELDS:
        counts = Counter(row.get(field, "") for row in policy_rows if row.get(field, ""))
        for value, count in sorted(counts.items()):
            summary.append({"code_category": field, "code_value": value, "count": count})
    return summary


def strength_bucket(value: str) -> str:
    return (value or "").strip().split("_", 1)[0]


def summarize_articles(article_rows: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    contribution_counts = Counter(
        row.get("primary_contribution_type", "")
        for row in article_rows
        if row.get("primary_contribution_type", "")
    )
    by_strength: dict[str, Counter] = defaultdict(Counter)
    for row in article_rows:
        strength = row.get("architectonic_strength", "")
        confidence = row.get("coding_confidence", "")
        if strength:
            by_strength[strength][confidence or "unspecified"] += 1

    strict_count = 0
    moderate_count = 0
    broad_structural_count = 0
    architectonic_or_operational_count = 0
    for row in article_rows:
        strength = strength_bucket(row.get("architectonic_strength", ""))
        confidence = (row.get("coding_confidence", "") or "").strip().lower()
        architecture_dependence = (row.get("architecture_dependence", "") or "").strip().lower()
        primary = (row.get("primary_contribution_type", "") or "").strip().lower()
        secondary = (row.get("secondary_contribution_type", "") or "").strip().lower()

        if strength in {"2", "3"} and architecture_dependence == "high" and confidence == "high":
            strict_count += 1
        if strength in {"2", "3"} and architecture_dependence in {"medium", "high"} and confidence in ARTICLE_CONFIDENCE_INCLUDED:
            moderate_count += 1
        if strength in {"1", "2", "3"} and architecture_dependence in {"medium", "high"} and confidence in ARTICLE_CONFIDENCE_INCLUDED:
            broad_structural_count += 1
        if confidence in ARTICLE_CONFIDENCE_INCLUDED and ({primary, secondary} & ARCHITECTONIC_PRIMARY_TYPES):
            architectonic_or_operational_count += 1

    contribution_rows = [
        {"primary_contribution_type": value, "count": count}
        for value, count in sorted(contribution_counts.items())
    ]
    strength_rows = []
    for strength, counter in sorted(by_strength.items()):
        for confidence, count in sorted(counter.items()):
            strength_rows.append(
                {
                    "architectonic_strength": strength,
                    "coding_confidence": confidence,
                    "count": count,
                }
            )

    sensitivity_rows = [
        {"definition_version": "strict_architectonic_article", "count": strict_count},
        {"definition_version": "strong_architectonic_article", "count": moderate_count},
        {"definition_version": "broad_structural_count", "count": broad_structural_count},
        {"definition_version": "architectonic_or_operational_article", "count": architectonic_or_operational_count},
    ]
    return contribution_rows, strength_rows, sensitivity_rows


def write_summary(sample_rows: list[dict], policy_rows: list[dict], article_rows: list[dict]) -> None:
    _, _, sensitivity_rows = summarize_articles(article_rows)
    sensitivity_lookup = {row["definition_version"]: row["count"] for row in sensitivity_rows}
    lines = [
        "# Results Summary",
        "",
        "This file is generated by `07_analysis/analysis.py`.",
        "",
        f"- Sampled journals: {sum(1 for row in sample_rows if row.get('sample_id') or row.get('journal_id') or row.get('journal_name'))}",
        f"- Policy-coded journals: {sum(1 for row in policy_rows if row.get('journal_id'))}",
        f"- Article-coded rows: {sum(1 for row in article_rows if row.get('article_id'))}",
        f"- Strict architectonic articles: {sensitivity_lookup.get('strict_architectonic_article', 0)}",
        f"- Strong architectonic articles: {sensitivity_lookup.get('strong_architectonic_article', 0)}",
        f"- Broad structural articles: {sensitivity_lookup.get('broad_structural_count', 0)}",
        f"- Architectonic or operational articles: {sensitivity_lookup.get('architectonic_or_operational_article', 0)}",
        "",
        "Sensitivity-analysis counts follow the thresholds defined in the article contribution codebook.",
    ]
    RESULTS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    sample_rows = read_rows(SAMPLE_PATH)
    policy_rows = read_rows(POLICY_PATH)
    article_rows = read_rows(ARTICLE_PATH)

    write_csv(
        TABLES_DIR / "table_1_journal_sample_by_category.csv",
        ["primary_category", "journal_count"],
        summarize_sample(sample_rows),
    )
    write_csv(
        TABLES_DIR / "table_2_policy_code_distribution.csv",
        ["code_category", "code_value", "count"],
        summarize_policy(policy_rows),
    )
    contribution_rows, strength_rows, sensitivity_rows = summarize_articles(article_rows)
    write_csv(
        TABLES_DIR / "table_4_contribution_types.csv",
        ["primary_contribution_type", "count"],
        contribution_rows,
    )
    write_csv(
        TABLES_DIR / "table_5_article_sensitivity_counts.csv",
        ["definition_version", "count"],
        sensitivity_rows,
    )
    write_csv(
        TABLES_DIR / "table_7_architectonic_strength_by_confidence.csv",
        ["architectonic_strength", "coding_confidence", "count"],
        strength_rows,
    )
    write_summary(sample_rows, policy_rows, article_rows)
    print(f"Wrote analysis outputs to {TABLES_DIR}")


if __name__ == "__main__":
    main()