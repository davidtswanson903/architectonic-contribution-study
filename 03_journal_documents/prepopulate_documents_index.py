from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = ROOT / "02_sampling" / "journal_sample.csv"
INDEX_PATH = Path(__file__).resolve().parent / "documents_index.csv"

FIELDNAMES = [
    "document_id",
    "journal_id",
    "journal_name",
    "document_type",
    "document_title",
    "url",
    "access_date",
    "source_snapshot_file_path",
    "full_page_screenshot_file_path",
    "relevant_excerpt_screenshot_file_path",
    "raw_text_file_path",
    "extracted_text_file_path",
    "extraction_method",
    "extraction_problem",
    "manual_extraction_notes",
    "collector",
    "source_snapshot_sha256",
    "full_page_screenshot_sha256",
    "relevant_excerpt_screenshot_sha256",
    "raw_text_sha256",
    "extracted_text_sha256",
    "notes",
]

DOCUMENT_TYPES = [
    "aims_scope",
    "submission_guidelines",
    "author_instructions",
    "reviewer_guidelines",
    "editorial_policy",
    "desk_rejection_policy",
    "article_types",
    "review_essay_policy",
    "special_issue_policy",
    "ethics_policy",
    "other",
]


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", (value or "").strip().lower())
    return normalized.strip("_") or "journal"


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def folder_name_for_row(sample_row: dict[str, str]) -> str:
    sample_id = (sample_row.get("sample_id") or "UNSAMPLED").strip() or "UNSAMPLED"
    journal_id = (sample_row.get("journal_id") or "NOJOURNALID").strip() or "NOJOURNALID"
    journal_slug = slugify(sample_row.get("journal_name", ""))
    return f"{sample_id}_{journal_id}_{journal_slug}"


def next_document_number(existing_rows: list[dict[str, str]]) -> int:
    max_number = 0
    for row in existing_rows:
        document_id = (row.get("document_id") or "").strip()
        if re.fullmatch(r"D\d{4}", document_id):
            max_number = max(max_number, int(document_id[1:]))
    return max_number + 1


def build_template_row(
    document_number: int,
    sample_row: dict[str, str],
    document_type: str,
    collector: str,
) -> dict[str, str]:
    document_id = f"D{document_number:04d}"
    folder_name = folder_name_for_row(sample_row)
    base_name = f"{document_id}_{document_type}"
    return {
        "document_id": document_id,
        "journal_id": sample_row.get("journal_id", ""),
        "journal_name": sample_row.get("journal_name", ""),
        "document_type": document_type,
        "document_title": "",
        "url": "",
        "access_date": "",
        "source_snapshot_file_path": f"raw/{folder_name}/source_snapshot/{base_name}_snapshot.html",
        "full_page_screenshot_file_path": f"raw/{folder_name}/screenshots/full_page/{base_name}_full_page.png",
        "relevant_excerpt_screenshot_file_path": f"raw/{folder_name}/screenshots/relevant_excerpt/{base_name}_excerpt.png",
        "raw_text_file_path": f"raw/{folder_name}/raw_text/{base_name}.txt",
        "extracted_text_file_path": f"extracted_text/{folder_name}/{base_name}.txt",
        "extraction_method": "",
        "extraction_problem": "",
        "manual_extraction_notes": "",
        "collector": collector,
        "source_snapshot_sha256": "",
        "full_page_screenshot_sha256": "",
        "relevant_excerpt_screenshot_sha256": "",
        "raw_text_sha256": "",
        "extracted_text_sha256": "",
        "notes": "Template row generated from the current journal sample.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepopulate documents_index.csv with template rows for each sampled journal and configured document type."
    )
    parser.add_argument("--sample-path", type=Path, default=SAMPLE_PATH, help="Path to the sampled journals CSV.")
    parser.add_argument("--index-path", type=Path, default=INDEX_PATH, help="Path to the documents index CSV.")
    parser.add_argument("--collector", default="", help="Optional collector name to prefill on generated rows.")
    args = parser.parse_args()

    sample_rows = [row for row in load_csv_rows(args.sample_path) if row.get("sample_id")]
    if not sample_rows:
        raise ValueError(f"No sampled journal rows found in {args.sample_path}")

    existing_rows = load_csv_rows(args.index_path)
    existing_pairs = {
        ((row.get("journal_id") or "").strip(), (row.get("document_type") or "").strip())
        for row in existing_rows
        if row.get("journal_id") and row.get("document_type")
    }

    new_rows: list[dict[str, str]] = []
    next_number = next_document_number(existing_rows)
    for sample_row in sample_rows:
        journal_id = (sample_row.get("journal_id") or "").strip()
        for document_type in DOCUMENT_TYPES:
            pair = (journal_id, document_type)
            if pair in existing_pairs:
                continue
            new_rows.append(build_template_row(next_number, sample_row, document_type, args.collector))
            existing_pairs.add(pair)
            next_number += 1

    all_rows = existing_rows + new_rows
    write_csv_rows(args.index_path, all_rows)

    print(f"Sample journals processed: {len(sample_rows)}")
    print(f"Existing index rows preserved: {len(existing_rows)}")
    print(f"Template rows added: {len(new_rows)}")
    print(f"Total index rows written: {len(all_rows)}")


if __name__ == "__main__":
    main()