from __future__ import annotations

import argparse
import csv
import hashlib
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = ROOT / "manifest.csv"
MANIFEST_FIELDNAMES = [
    "file_id",
    "file_name",
    "file_path",
    "file_role",
    "sha256_hash",
    "created_date",
    "modified_date",
    "generated_by",
    "notes",
]


def sha256_for_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest() -> list[dict[str, str]]:
    with MANIFEST_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_manifest(rows: list[dict[str, str]]) -> None:
    with MANIFEST_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDNAMES, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)


def write_sidecar(target_path: Path, digest: str) -> None:
    sidecar_path = target_path.parent / f"{target_path.name}.sha256"
    sidecar_path.write_text(f"{digest} *{target_path.name}", encoding="utf-8")


def refresh_manifest(note: str | None) -> tuple[int, str]:
    rows = load_manifest()
    today = date.today().isoformat()

    for row in rows:
        relative_path = Path(row["file_path"])
        absolute_path = ROOT / relative_path
        if not absolute_path.exists():
            raise FileNotFoundError(f"Manifest entry does not exist: {relative_path}")

        digest = sha256_for_file(absolute_path)
        row["sha256_hash"] = digest
        row["modified_date"] = today
        if note is not None:
            row["notes"] = note
        write_sidecar(absolute_path, digest)

    write_manifest(rows)
    manifest_digest = sha256_for_file(MANIFEST_PATH)
    write_sidecar(MANIFEST_PATH, manifest_digest)
    (ROOT / "manifest.sha256").write_text(f"{manifest_digest} *manifest.csv", encoding="utf-8")
    return len(rows), manifest_digest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Refresh manifest.csv hashes and per-file SHA-256 sidecars for tracked research artifacts."
    )
    parser.add_argument(
        "--note",
        help="Optional note to write into the manifest notes column for all tracked files.",
    )
    args = parser.parse_args()

    count, manifest_digest = refresh_manifest(args.note)
    print(f"Refreshed manifest entries: {count}")
    print(f"manifest.csv sha256: {manifest_digest}")


if __name__ == "__main__":
    main()