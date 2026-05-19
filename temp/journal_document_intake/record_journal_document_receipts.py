from __future__ import annotations

import argparse
import csv
import hashlib
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INDEX_PATH = ROOT / "03_journal_documents" / "documents_index.csv"
SAMPLE_PATH = ROOT / "02_sampling" / "journal_sample.csv"

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

ARTIFACT_SPECS = {
    "source_snapshot": {
        "input_key": "source_snapshot_input_path",
        "path_field": "source_snapshot_file_path",
        "hash_field": "source_snapshot_sha256",
        "subdir": Path("source_snapshot"),
        "suffix_tag": "snapshot",
    },
    "full_page_screenshot": {
        "input_key": "full_page_screenshot_input_path",
        "path_field": "full_page_screenshot_file_path",
        "hash_field": "full_page_screenshot_sha256",
        "subdir": Path("screenshots") / "full_page",
        "suffix_tag": "full_page",
    },
    "relevant_excerpt_screenshot": {
        "input_key": "relevant_excerpt_screenshot_input_path",
        "path_field": "relevant_excerpt_screenshot_file_path",
        "hash_field": "relevant_excerpt_screenshot_sha256",
        "subdir": Path("screenshots") / "relevant_excerpt",
        "suffix_tag": "excerpt",
    },
    "raw_text": {
        "input_key": "raw_text_input_path",
        "path_field": "raw_text_file_path",
        "hash_field": "raw_text_sha256",
        "subdir": Path("raw_text"),
        "suffix_tag": "",
    },
    "extracted_text": {
        "input_key": "extracted_text_input_path",
        "path_field": "extracted_text_file_path",
        "hash_field": "extracted_text_sha256",
        "subdir": Path("."),
        "suffix_tag": "",
    },
}


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


def next_document_number(rows: list[dict[str, str]]) -> int:
    max_number = 0
    for row in rows:
        document_id = (row.get("document_id") or "").strip()
        if re.fullmatch(r"D\d{4}", document_id):
            max_number = max(max_number, int(document_id[1:]))
    return max_number + 1


def sample_lookup() -> dict[str, dict[str, str]]:
    return {
        (row.get("journal_id") or "").strip(): row
        for row in load_csv_rows(SAMPLE_PATH)
        if row.get("journal_id")
    }


def infer_journal_name(record: dict[str, str], sample_rows: dict[str, dict[str, str]]) -> str:
    explicit = (record.get("journal_name") or "").strip()
    if explicit:
        return explicit
    journal_id = (record.get("journal_id") or "").strip()
    if journal_id in sample_rows:
        return (sample_rows[journal_id].get("journal_name") or "").strip()
    return ""


def folder_name_for_record(record: dict[str, str], sample_rows: dict[str, dict[str, str]]) -> str:
    journal_id = (record.get("journal_id") or "").strip()
    if journal_id in sample_rows:
        sample_row = sample_rows[journal_id]
        sample_id = (sample_row.get("sample_id") or "TEMP").strip() or "TEMP"
        journal_name = sample_row.get("journal_name", "") or record.get("journal_name", "")
        return f"{sample_id}_{journal_id}_{slugify(journal_name)}"
    journal_name = record.get("journal_name", "")
    return f"TEMP_{journal_id or 'NOJOURNALID'}_{slugify(journal_name)}"


def resolve_input_path(raw_path: str, base_dir: Path) -> Path | None:
    candidate = (raw_path or "").strip()
    if not candidate:
        return None
    resolved = Path(candidate)
    if not resolved.is_absolute():
        resolved = (base_dir / resolved).resolve()
    return resolved


def sha256_for_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_destination_relative_path(record: dict[str, str], artifact_key: str, source_path: Path, sample_rows: dict[str, dict[str, str]]) -> str:
    spec = ARTIFACT_SPECS[artifact_key]
    document_id = (record.get("document_id") or "").strip()
    raw_document_type = (record.get("document_type") or "").strip()
    document_type = slugify(raw_document_type) if raw_document_type else "raw_artifact"
    folder_name = folder_name_for_record(record, sample_rows)
    suffix = source_path.suffix.lower() or ".bin"
    base_name = f"{document_id}_{document_type}"

    if artifact_key == "extracted_text":
        filename = f"{base_name}{suffix}"
        return str(Path("extracted_text") / folder_name / filename).replace("\\", "/")

    if artifact_key == "raw_text":
        filename = f"{base_name}{suffix}"
        return str(Path("raw") / folder_name / spec["subdir"] / filename).replace("\\", "/")

    tag = spec["suffix_tag"]
    filename = f"{base_name}_{tag}{suffix}"
    return str(Path("raw") / folder_name / spec["subdir"] / filename).replace("\\", "/")


def ensure_parent(path: Path, dry_run: bool) -> None:
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)


def find_existing_row(rows: list[dict[str, str]], record: dict[str, str]) -> dict[str, str] | None:
    document_id = (record.get("document_id") or "").strip()
    if document_id:
        for row in rows:
            if (row.get("document_id") or "").strip() == document_id:
                return row
    return None


def blank_row() -> dict[str, str]:
    return {field: "" for field in FIELDNAMES}


def ingest_record(
    rows: list[dict[str, str]],
    record: dict[str, str],
    base_dir: Path,
    sample_rows: dict[str, dict[str, str]],
    next_number: int,
    dry_run: bool,
) -> tuple[int, bool]:
    row = find_existing_row(rows, record)
    created = False
    if row is None:
        row = blank_row()
        row["document_id"] = f"D{next_number:04d}"
        next_number += 1
        rows.append(row)
        created = True

    if not (record.get("journal_id") or row.get("journal_id")):
        raise ValueError("journal_id is required")
    inferred_journal_name = infer_journal_name(record, sample_rows)
    if inferred_journal_name and not row.get("journal_name"):
        row["journal_name"] = inferred_journal_name
    if not (record.get("journal_name") or row.get("journal_name") or inferred_journal_name):
        raise ValueError("journal_name is required")

    for field in [
        "journal_id",
        "journal_name",
        "document_type",
        "document_title",
        "url",
        "access_date",
        "extraction_method",
        "extraction_problem",
        "manual_extraction_notes",
        "collector",
        "notes",
    ]:
        value = (record.get(field) or "").strip()
        if value:
            row[field] = value

    for artifact_key, spec in ARTIFACT_SPECS.items():
        source_path = resolve_input_path(record.get(spec["input_key"], ""), base_dir)
        if source_path is None:
            continue
        if not source_path.exists():
            raise FileNotFoundError(f"Artifact path does not exist: {source_path}")

        relative_destination = build_destination_relative_path(row, artifact_key, source_path, sample_rows)
        absolute_destination = ROOT / "03_journal_documents" / Path(relative_destination)
        if artifact_key == "extracted_text":
            absolute_destination = ROOT / Path("03_journal_documents") / Path(relative_destination)

        ensure_parent(absolute_destination, dry_run)
        if not dry_run:
            shutil.copy2(source_path, absolute_destination)
            digest = sha256_for_file(absolute_destination)
        else:
            digest = sha256_for_file(source_path)

        row[spec["path_field"]] = relative_destination
        row[spec["hash_field"]] = digest

    return next_number, created


def cli_record_from_args(args: argparse.Namespace) -> dict[str, str]:
    raw_text_input = args.raw_text or args.extracted_text or ""
    return {
        "document_id": args.document_id or "",
        "journal_id": args.journal_id or "",
        "journal_name": args.journal_name or "",
        "document_type": args.document_type or "",
        "document_title": args.document_title or "",
        "url": args.url or "",
        "access_date": args.access_date or "",
        "extraction_method": args.extraction_method or "",
        "extraction_problem": args.extraction_problem or "",
        "manual_extraction_notes": args.manual_extraction_notes or "",
        "collector": args.collector or "",
        "notes": args.notes or "",
        "source_snapshot_input_path": args.source_snapshot or "",
        "full_page_screenshot_input_path": args.full_page_screenshot or "",
        "relevant_excerpt_screenshot_input_path": args.relevant_excerpt_screenshot or "",
        "raw_text_input_path": raw_text_input,
        "extracted_text_input_path": "",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest one or more journal document artifacts from a temp workspace into the canonical collection structure and documents index."
    )
    parser.add_argument("--batch-csv", type=Path, help="Optional batch CSV with one row per document record.")
    parser.add_argument("--document-id")
    parser.add_argument("--journal-id")
    parser.add_argument("--journal-name")
    parser.add_argument("--document-type")
    parser.add_argument("--document-title")
    parser.add_argument("--url")
    parser.add_argument("--access-date")
    parser.add_argument("--extraction-method")
    parser.add_argument("--extraction-problem")
    parser.add_argument("--manual-extraction-notes")
    parser.add_argument("--collector")
    parser.add_argument("--notes")
    parser.add_argument("--source-snapshot")
    parser.add_argument("--full-page-screenshot")
    parser.add_argument("--relevant-excerpt-screenshot")
    parser.add_argument("--raw-text")
    parser.add_argument("--extracted-text", help="Deprecated alias for --raw-text during the raw-receipt phase.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and resolve destinations without writing files or changing the index.")
    args = parser.parse_args()

    rows = load_csv_rows(INDEX_PATH)
    sample_rows = sample_lookup()
    next_number = next_document_number(rows)

    if args.batch_csv:
        batch_rows = load_csv_rows(args.batch_csv)
        if not batch_rows:
            raise ValueError(f"No batch rows found in {args.batch_csv}")
        records = batch_rows
        base_dir = args.batch_csv.resolve().parent
    else:
        records = [cli_record_from_args(args)]
        base_dir = Path.cwd()

    created_rows = 0
    for record in records:
        next_number, created = ingest_record(rows, record, base_dir, sample_rows, next_number, args.dry_run)
        if created:
            created_rows += 1

    if not args.dry_run:
        write_csv_rows(INDEX_PATH, rows)

    print(f"Records processed: {len(records)}")
    print(f"New index rows created: {created_rows}")
    print(f"Index write mode: {'dry_run' if args.dry_run else 'applied'}")


if __name__ == "__main__":
    main()