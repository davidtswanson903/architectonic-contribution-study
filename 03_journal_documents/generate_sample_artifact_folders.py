from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = ROOT / "02_sampling" / "journal_sample.csv"
RAW_ROOT = Path(__file__).resolve().parent / "raw"
EXTRACTED_ROOT = Path(__file__).resolve().parent / "extracted_text"


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", (value or "").strip().lower())
    return normalized.strip("_") or "journal"


def load_sample_rows(sample_path: Path) -> list[dict[str, str]]:
    with sample_path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def folder_name_for_row(row: dict[str, str]) -> str:
    sample_id = (row.get("sample_id") or "UNSAMPLED").strip() or "UNSAMPLED"
    journal_id = (row.get("journal_id") or "NOJOURNALID").strip() or "NOJOURNALID"
    journal_slug = slugify(row.get("journal_name", ""))
    return f"{sample_id}_{journal_id}_{journal_slug}"


def ensure_folder(path: Path) -> bool:
    existed = path.exists()
    path.mkdir(parents=True, exist_ok=True)
    return not existed


def ensure_collection_structure(raw_root: Path, extracted_root: Path, folder_name: str, raw_only: bool) -> tuple[int, int, int]:
    raw_journal_folder_created = 0
    raw_support_folders_created = 0
    extracted_journal_folder_created = 0

    journal_raw_path = raw_root / folder_name
    if ensure_folder(journal_raw_path):
        raw_journal_folder_created = 1

    raw_paths = [
        journal_raw_path / "source_snapshot",
        journal_raw_path / "raw_text",
        journal_raw_path / "screenshots",
        journal_raw_path / "screenshots" / "full_page",
        journal_raw_path / "screenshots" / "relevant_excerpt",
    ]
    for path in raw_paths:
        if ensure_folder(path):
            raw_support_folders_created += 1

    if not raw_only and ensure_folder(extracted_root / folder_name):
        extracted_journal_folder_created = 1

    return raw_journal_folder_created, raw_support_folders_created, extracted_journal_folder_created


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate per-sampled-journal folders for raw journal artifacts and extracted text "
            "using the current journal sample."
        )
    )
    parser.add_argument(
        "--sample-path",
        type=Path,
        default=SAMPLE_PATH,
        help="Path to the sampled journals CSV. Defaults to 02_sampling/journal_sample.csv.",
    )
    parser.add_argument(
        "--raw-root",
        type=Path,
        default=RAW_ROOT,
        help="Root folder for raw journal artifact directories.",
    )
    parser.add_argument(
        "--extracted-root",
        type=Path,
        default=EXTRACTED_ROOT,
        help="Root folder for extracted-text directories.",
    )
    parser.add_argument(
        "--raw-only",
        action="store_true",
        help="Only create raw artifact folders and skip extracted-text folders.",
    )
    args = parser.parse_args()

    sample_rows = [row for row in load_sample_rows(args.sample_path) if row.get("sample_id")]
    if not sample_rows:
        raise ValueError(f"No sampled journal rows found in {args.sample_path}")

    raw_journal_folders_created = 0
    raw_support_folders_created = 0
    extracted_journal_folders_created = 0
    for row in sample_rows:
        folder_name = folder_name_for_row(row)
        created_raw_journal, created_raw_support, created_extracted = ensure_collection_structure(
            args.raw_root,
            args.extracted_root,
            folder_name,
            args.raw_only,
        )
        raw_journal_folders_created += created_raw_journal
        raw_support_folders_created += created_raw_support
        extracted_journal_folders_created += created_extracted

    print(f"Sample rows processed: {len(sample_rows)}")
    print(f"Raw journal folders created: {raw_journal_folders_created}")
    print(f"Raw support subfolders created: {raw_support_folders_created}")
    if args.raw_only:
        print("Extracted-text folders skipped (--raw-only).")
    else:
        print(f"Extracted-text journal folders created: {extracted_journal_folders_created}")


if __name__ == "__main__":
    main()