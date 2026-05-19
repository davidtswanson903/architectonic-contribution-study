from __future__ import annotations

import csv
import json
import math
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
    with UNIVERSE_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_flag(value: str) -> str:
    return (value or "").strip().lower()


def z_score_for_confidence(confidence_level: float) -> float:
    supported = {
        0.9: 1.645,
        0.95: 1.96,
        0.99: 2.576,
    }
    normalized = round(float(confidence_level), 2)
    if normalized not in supported:
        raise ValueError(f"Unsupported confidence_level: {confidence_level}")
    return supported[normalized]


def finite_population_sample_size(population_size: int, config: dict) -> tuple[int, float, float, float]:
    if population_size <= 0:
        raise ValueError("Population size must be positive to compute a sample size.")

    confidence_level = float(config.get("confidence_level", 0.95))
    response_distribution = float(config.get("response_distribution", 0.5))
    target_margin = float(config.get("target_margin_of_error", 0.1))
    z_score = z_score_for_confidence(confidence_level)
    initial_size = (z_score**2 * response_distribution * (1 - response_distribution)) / (target_margin**2)
    adjusted_size = initial_size / (1 + ((initial_size - 1) / population_size))
    return math.ceil(adjusted_size), initial_size, adjusted_size, z_score


def filter_universe(rows: list[dict], config: dict) -> list[dict]:
    language_field = str(config.get("language_eligible_field", "included_in_language_eligible_population"))
    require_language_eligible = bool(config.get("require_language_eligible_population", False))
    filtered = []
    for row in rows:
        if normalize_flag(row.get("included_in_sampling_frame")) != "yes":
            continue
        if require_language_eligible and normalize_flag(row.get(language_field)) != "yes":
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


def get_active_strata(grouped: dict[str, list[dict]], config: dict) -> list[str]:
    configured = [str(item).strip().lower() for item in config.get("strata", []) if str(item).strip()]
    available = [stratum for stratum in configured if grouped.get(stratum)]
    if available:
        return available
    return sorted(stratum for stratum, rows in grouped.items() if rows)


def allocate_targets(grouped: dict[str, list[dict]], strata: list[str], target_size: int, allocation_strategy: str) -> dict[str, int]:
    if not strata or target_size <= 0:
        return {}

    if allocation_strategy != "proportional":
        base_take = target_size // len(strata)
        remainder = target_size % len(strata)
        return {stratum: base_take + (1 if index < remainder else 0) for index, stratum in enumerate(strata)}

    total_available = sum(len(grouped[stratum]) for stratum in strata)
    if total_available == 0:
        return {stratum: 0 for stratum in strata}

    exact_targets = {
        stratum: target_size * len(grouped[stratum]) / total_available
        for stratum in strata
    }
    allocated = {stratum: math.floor(value) for stratum, value in exact_targets.items()}
    remainder = target_size - sum(allocated.values())
    ranked_remainders = sorted(
        ((exact_targets[stratum] - allocated[stratum], stratum) for stratum in strata),
        key=lambda item: (-item[0], item[1]),
    )
    for _, stratum in ranked_remainders[:remainder]:
        allocated[stratum] += 1
    return allocated


def stratified_sample(rows: list[dict], config: dict) -> list[dict]:
    configured_size = config.get("sample_size")
    if configured_size in (None, "") and config.get("auto_calculate_sample_size", False):
        target_size, _, _, _ = finite_population_sample_size(len(rows), config)
    else:
        target_size = int(config.get("sample_size", 0))
    if target_size <= 0:
        return []

    rng = random.Random(int(config["seed"]))
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[(row.get("primary_category") or "unclear").strip().lower()].append(row)

    strata = get_active_strata(grouped, config)
    allocation_strategy = str(config.get("allocation_strategy", "equal")).strip().lower()
    target_counts = allocate_targets(grouped, strata, target_size, allocation_strategy)

    selected: list[dict] = []

    leftovers: list[dict] = []
    for stratum in strata:
        bucket = list(grouped.get(stratum, []))
        rng.shuffle(bucket)
        desired = min(target_counts.get(stratum, 0), len(bucket))
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
    calculated_sample_size = ""
    initial_size = ""
    adjusted_size = ""
    z_score = ""
    if config.get("auto_calculate_sample_size", False) and eligible_rows > 0:
        calculated_sample_size, initial_size, adjusted_size, z_score = finite_population_sample_size(eligible_rows, config)
    lines = [
        f"timestamp_utc: {datetime.now(timezone.utc).isoformat()}",
        f"seed: {config.get('seed', '')}",
        f"sampling_method: {config.get('sampling_method', '')}",
        f"allocation_strategy: {config.get('allocation_strategy', '')}",
        f"require_language_eligible_population: {config.get('require_language_eligible_population', False)}",
        f"language_eligible_field: {config.get('language_eligible_field', '')}",
        f"configured_sample_size: {config.get('sample_size', '')}",
        f"population_size: {config.get('population_size', '')}",
        f"confidence_level: {config.get('confidence_level', '')}",
        f"response_distribution: {config.get('response_distribution', '')}",
        f"target_margin_of_error: {config.get('target_margin_of_error', '')}",
        f"sample_size_formula: {config.get('sample_size_formula', '')}",
        f"sample_size_rationale: {config.get('sample_size_rationale', '')}",
        f"z_score: {z_score}",
        f"unadjusted_sample_size_n0: {initial_size}",
        f"finite_population_adjusted_n: {adjusted_size}",
        f"calculated_sample_size: {calculated_sample_size}",
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
    if config.get("require_language_eligible_population", False) and not eligible_rows:
        raise ValueError(
            "No journals passed the configured language-eligibility filter. Populate "
            "included_in_language_eligible_population before sampling."
        )

    if config.get("auto_calculate_sample_size", False) and eligible_rows:
        target_size, initial_size, adjusted_size, _ = finite_population_sample_size(len(eligible_rows), config)
        config["population_size"] = len(eligible_rows)
        config["sample_size"] = target_size
        config["sample_size_rationale"] = (
            "Finite-population sample for the filtered language-eligible journal population "
            f"N={len(eligible_rows)}, confidence={config.get('confidence_level', '')}, "
            f"p={config.get('response_distribution', '')}, margin={config.get('target_margin_of_error', '')}. "
            f"Exact n0={initial_size:.4f}, adjusted n={adjusted_size:.4f}, rounded up to {target_size}."
        )
    sampled_rows = stratified_sample(eligible_rows, config)
    write_sample(sampled_rows, config)
    write_log(len(all_rows), len(eligible_rows), sampled_rows, config)
    print(f"Wrote {len(sampled_rows)} sampled journals to {SAMPLE_PATH}")


if __name__ == "__main__":
    main()