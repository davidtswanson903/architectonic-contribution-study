from __future__ import annotations

import csv
import json
import random
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNIVERSE_PATH = ROOT / "01_journal_universe" / "journal_universe_clean.csv"
CONFIG_PATH = Path(__file__).with_name("sample_config.json")
SAMPLE_PATH = Path(__file__).with_name("journal_sample.csv")
LOG_PATH = Path(__file__).with_name("sample_log.txt")

OUTPUT_FIELDS = [
    "sample_id",
    "journal_id",
    "journal_name",
    "primary_category",
    "secondary_category",
    "journal_url",
    "sampling_stratum",
    "sample_method",
    "seed",
    "date_sampled",
]


def load_config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_universe() -> list[dict]:
    with UNIVERSE_PATH.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_flag(value: str) -> str:
    return (value or "").strip().lower()


def filter_universe(rows: list[dict], config: dict) -> list[dict]:
    filtered = []
    for row in rows:
        if normalize_flag(row.get("included_in_sampling_frame")) != "yes":
            continue
        if config.get("include_only_active_peer_reviewed", True):
            if normalize_flag(row.get("peer_reviewed")) != "yes":
                continue
            if normalize_flag(row.get("active_status")) != "active":
                continue
        if normalize_flag(row.get("publishes_research_articles")) != "yes":
            continue
        filtered.append(row)
    return filtered


def stratified_sample(rows: list[dict], config: dict) -> list[dict]:
    target_size = int(config.get("sample_size", 0))
    if target_size <= 0:
        return []

    rng = random.Random(int(config["seed"]))
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[(row.get("primary_category") or "unclear").strip().lower()].append(row)

    strata = [str(item).strip().lower() for item in config.get("strata", []) if str(item).strip()]
    if not strata:
        strata = sorted(grouped)

    selected: list[dict] = []
    base_take = target_size // len(strata) if strata else target_size
    remainder = target_size % len(strata) if strata else 0

    leftovers: list[dict] = []
    for index, stratum in enumerate(strata):
        bucket = list(grouped.get(stratum, []))
        rng.shuffle(bucket)
        desired = base_take + (1 if index < remainder else 0)
        selected.extend(bucket[:desired])
        leftovers.extend(bucket[desired:])

    if len(selected) < target_size:
        unsampled_ids = {row.get("journal_id") for row in selected}
        for row in rows:
            if row.get("journal_id") not in unsampled_ids and row not in leftovers:
                leftovers.append(row)
        rng.shuffle(leftovers)
        selected.extend(leftovers[: target_size - len(selected)])

    selected.sort(key=lambda row: (row.get("primary_category", ""), row.get("journal_name", "")))
    return selected[:target_size]


def write_sample(rows: list[dict], config: dict) -> None:
    sampled_on = date.today().isoformat()
    with SAMPLE_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        for index, row in enumerate(rows, start=1):
            writer.writerow(
                {
                    "sample_id": f"S{index:04d}",
                    "journal_id": row.get("journal_id", ""),
                    "journal_name": row.get("journal_name", ""),
                    "primary_category": row.get("primary_category", ""),
                    "secondary_category": row.get("secondary_category", ""),
                    "journal_url": row.get("journal_url", ""),
                    "sampling_stratum": row.get("primary_category", ""),
                    "sample_method": config.get("sampling_method", ""),
                    "seed": config.get("seed", ""),
                    "date_sampled": sampled_on,
                }
            )


def write_log(total_rows: int, eligible_rows: int, sampled_rows: list[dict], config: dict) -> None:
    lines = [
        f"timestamp_utc: {datetime.now(timezone.utc).isoformat()}",
        f"seed: {config.get('seed', '')}",
        f"sampling_method: {config.get('sampling_method', '')}",
        f"configured_sample_size: {config.get('sample_size', '')}",
        f"journal_universe_rows: {total_rows}",
        f"eligible_rows: {eligible_rows}",
        f"sampled_rows: {len(sampled_rows)}",
    ]
    counts: dict[str, int] = defaultdict(int)
    for row in sampled_rows:
        counts[row.get("primary_category", "unclear")] += 1
    for stratum, count in sorted(counts.items()):
        lines.append(f"stratum_{stratum}: {count}")

    LOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    config = load_config()
    all_rows = load_universe()
    eligible_rows = filter_universe(all_rows, config)
    sampled_rows = stratified_sample(eligible_rows, config)
    write_sample(sampled_rows, config)
    write_log(len(all_rows), len(eligible_rows), sampled_rows, config)
    print(f"Wrote {len(sampled_rows)} sampled journals to {SAMPLE_PATH}")


if __name__ == "__main__":
    main()