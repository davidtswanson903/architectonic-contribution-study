from __future__ import annotations

import base64
import csv
import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNIVERSE_PATH = ROOT / "01_journal_universe" / "journal_universe_clean.csv"
EXCLUSIONS_PATH = ROOT / "01_journal_universe" / "journal_universe_exclusions.csv"
PROFILE_DATA_URL = (
    "https://www.pjip.org/uploads/1/4/8/0/148077507/custom_themes/"
    "727891833533859441/files/z_en_Philosophy.json"
)
PROFILE_DATA_SALT = "4jri23jru283rf"
PROFILE_SUBJECT_KEY = "Philosophy"
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; GitHub-Copilot-Language-Audit/1.0)",
    "Accept-Language": "en-US,en;q=0.9",
}
LANGUAGE_NAME_MAP = {
    "ENG": "English",
    "SPA": "Spanish",
    "POR": "Portuguese",
    "FRA": "French",
    "GER": "German",
    "ITA": "Italian",
    "POL": "Polish",
    "RUS": "Russian",
    "JPN": "Japanese",
    "CHI": "Chinese",
    "ZHO": "Chinese",
    "KOR": "Korean",
    "CRO": "Croatian",
    "CZE": "Czech",
    "HUN": "Hungarian",
    "NLD": "Dutch",
    "SWE": "Swedish",
    "NOR": "Norwegian",
    "DAN": "Danish",
    "FIN": "Finnish",
    "GRE": "Greek",
    "ELL": "Greek",
    "TUR": "Turkish",
    "ROM": "Romanian",
    "RON": "Romanian",
    "CAT": "Catalan",
    "LAT": "Latin",
}
LANGUAGE_CODE_ALIASES = {
    "ENGLISH": "ENG",
    "ENG": "ENG",
    "FR": "FRA",
    "FRE": "FRA",
    "FRA": "FRA",
    "FRENCH": "FRA",
    "DE": "GER",
    "DEU": "GER",
    "GER": "GER",
    "GERMAN": "GER",
    "IT": "ITA",
    "ITA": "ITA",
    "ITALIAN": "ITA",
    "ES": "SPA",
    "SPA": "SPA",
    "SPANISH": "SPA",
    "PT": "POR",
    "POR": "POR",
    "PORTUGUESE": "POR",
    "RU": "RUS",
    "RUS": "RUS",
    "RUSSIAN": "RUS",
    "CES": "CZE",
    "CZE": "CZE",
    "CZECH": "CZE",
    "SLK": "SLK",
    "SLOVAK": "SLK",
    "POL": "POL",
    "POLISH": "POL",
    "NL": "NLD",
    "NLD": "NLD",
    "DUTCH": "NLD",
    "RECOMMENDED": "",
}
ENGLISH_POLICY_KEYWORDS = (
    "submission",
    "submissions",
    "manuscript",
    "manuscripts",
    "author",
    "authors",
    "guideline",
    "guidelines",
    "article",
    "articles",
    "peer review",
    "peer-review",
    "abstract",
)
CSV_FIELD_ORDER = [
    "journal_id",
    "journal_name",
    "publisher",
    "journal_url",
    "issn_print",
    "issn_online",
    "primary_category",
    "secondary_category",
    "language",
    "language_status",
    "primary_publication_language",
    "english_policy_available",
    "english_articles_available",
    "language_exclusion_reason",
    "included_in_language_eligible_population",
    "peer_reviewed",
    "active_status",
    "publishes_research_articles",
    "included_in_sampling_frame",
    "inclusion_reason",
    "exclusion_reason",
    "source_id",
    "date_verified",
    "notes",
]


@dataclass
class LinkTargets:
    homepage_url: str = ""
    guidelines_url: str = ""


class AnchorExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._current_href = ""
        self._current_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        self._current_href = dict(attrs).get("href", "") or ""
        self._current_text = []

    def handle_data(self, data: str) -> None:
        if self._current_href:
            self._current_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "a" or not self._current_href:
            return
        text = " ".join(part.strip() for part in self._current_text if part.strip()).strip()
        self.links.append((text.lower(), self._current_href.strip()))
        self._current_href = ""
        self._current_text = []


def fetch_text(url: str, timeout: int = 20) -> str:
    request = urllib.request.Request(url, headers=REQUEST_HEADERS)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def decode_profile_payload() -> dict[str, dict]:
    raw_payload = fetch_text(PROFILE_DATA_URL)
    outer = json.loads(raw_payload)
    encoded = outer["encoded"].replace(PROFILE_DATA_SALT, "")
    decoded = base64.b64decode(encoded).decode("utf-8")
    parsed = json.loads(decoded)
    records = parsed.get(PROFILE_SUBJECT_KEY, [])
    return {str(record.get("eISSN", "")).strip(): record for record in records if record.get("eISSN")}


def parse_links(html_fragment: str) -> LinkTargets:
    parser = AnchorExtractor()
    parser.feed(html_fragment or "")
    targets = LinkTargets()
    for label, href in parser.links:
        if label == "homepage" and not targets.homepage_url:
            targets.homepage_url = href
        elif label == "submission guidelines" and not targets.guidelines_url:
            targets.guidelines_url = href
        elif label == "guidelines" and not targets.guidelines_url:
            targets.guidelines_url = href
    return targets


def parse_language_codes(value: str) -> list[str]:
    normalized_codes: list[str] = []
    for token in re.findall(r"[A-Za-z]+", value or ""):
        mapped = LANGUAGE_CODE_ALIASES.get(token.upper(), token.upper())
        if not mapped:
            continue
        if mapped not in normalized_codes:
            normalized_codes.append(mapped)
    return normalized_codes


def render_language_names(codes: list[str]) -> str:
    names = [LANGUAGE_NAME_MAP.get(code, code.title()) for code in codes]
    return "; ".join(names)


def classify_language_status(codes: list[str]) -> str:
    if not codes:
        return "unclear"
    if codes == ["ENG"]:
        return "english_primary"
    if "ENG" in codes:
        return "multilingual_english_available"
    return "non_english_primary"


def detect_english_policy(*urls: str) -> tuple[str, str]:
    candidates = [url for url in urls if url]
    if not candidates:
        return "unclear", "no_policy_link"

    last_basis = "no_policy_link"
    for index, url in enumerate(candidates):
        source_label = "guidelines" if index == 0 else "homepage"
        try:
            html = fetch_text(url, timeout=15)
        except (TimeoutError, urllib.error.URLError, ValueError) as error:
            last_basis = f"{source_label}_fetch_failed:{type(error).__name__}"
            continue

        lowered = re.sub(r"\s+", " ", html).lower()
        keyword_hits = sum(1 for keyword in ENGLISH_POLICY_KEYWORDS if keyword in lowered)
        lang_match = re.search(r"<html[^>]*\slang=[\"']([^\"']+)[\"']", lowered)
        if lang_match and lang_match.group(1).startswith("en"):
            return "yes", f"{source_label}_html_lang_en"
        if keyword_hits >= 4:
            return "yes", f"{source_label}_english_policy_keywords={keyword_hits}"
        last_basis = f"{source_label}_keywords={keyword_hits}"
    return "unclear", last_basis


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    normalized_rows: list[dict[str, str]] = []
    for row in rows:
        normalized_rows.append(
            {
                (key or "").lstrip("\ufeff").strip().strip('"'): value
                for key, value in row.items()
            }
        )
    return normalized_rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def preserve(existing_value: str, generated_value: str) -> str:
    return existing_value if (existing_value or "").strip() else generated_value


def preserve_manual(existing_value: str, generated_value: str, placeholders: set[str] | None = None) -> str:
    current = (existing_value or "").strip()
    if not current:
        return generated_value
    placeholder_values = placeholders or {"unclear"}
    if current.lower() in placeholder_values:
        return generated_value
    return existing_value


def merge_note(existing_note: str, audit_note: str) -> str:
    existing = (existing_note or "").strip()
    if not audit_note:
        return existing
    if audit_note in existing:
        return existing
    if not existing:
        return audit_note
    return f"{existing}; {audit_note}"


def main() -> None:
    universe_rows = read_csv(UNIVERSE_PATH)
    profile_records = decode_profile_payload()

    updated_rows: list[dict[str, str]] = []
    generated_exclusions: dict[str, dict[str, str]] = {}
    coded_count = 0
    included_count = 0
    excluded_count = 0

    for row in universe_rows:
        updated = dict(row)
        issn = (row.get("issn_online") or "").strip()
        profile = profile_records.get(issn, {})
        raw_language = str(profile.get("Language", "")).strip()
        codes = parse_language_codes(raw_language)
        language_status = classify_language_status(codes)
        primary_language = render_language_names(codes)
        links = parse_links(str(profile.get("JournalPageTitle", "")))
        policy_status, policy_basis = detect_english_policy(links.guidelines_url, links.homepage_url)

        if language_status == "english_primary":
            english_articles_available = "yes"
        elif language_status == "multilingual_english_available":
            english_articles_available = "yes"
        elif language_status == "non_english_primary":
            english_articles_available = "no"
        else:
            english_articles_available = "unclear"

        if language_status == "non_english_primary":
            included = "no"
            exclusion_reason = "non_english_primary"
        elif english_articles_available == "yes" and policy_status == "yes":
            included = "yes"
            exclusion_reason = ""
        elif language_status == "unclear" or policy_status == "unclear":
            included = ""
            exclusion_reason = ""
        else:
            included = "no"
            exclusion_reason = "english_policy_unavailable"

        updated["language"] = raw_language
        updated["language_status"] = language_status
        updated["primary_publication_language"] = primary_language
        updated["english_policy_available"] = policy_status
        updated["english_articles_available"] = english_articles_available
        updated["language_exclusion_reason"] = exclusion_reason
        updated["included_in_language_eligible_population"] = included

        audit_note = ""
        if raw_language:
            audit_note = f"pjip_language={raw_language}"
        if policy_basis:
            audit_note = merge_note(audit_note, f"policy_basis={policy_basis}")
        updated["notes"] = merge_note(updated.get("notes", ""), audit_note)

        final_included = (updated.get("included_in_language_eligible_population", "") or "").strip().lower()
        if final_included:
            coded_count += 1
        if final_included == "yes":
            included_count += 1
        elif final_included == "no":
            excluded_count += 1
            journal_id = updated.get("journal_id", "")
            generated_exclusions[journal_id] = {
                "journal_id": journal_id,
                "journal_name": updated.get("journal_name", ""),
                "exclusion_reason": updated.get("language_exclusion_reason", "") or "language_ineligible",
                "evidence_basis": f"PJIP Language={raw_language or 'missing'}; {policy_basis}",
                "date_excluded": updated.get("date_verified", ""),
                "notes": "Excluded because coding cannot be performed reliably in English.",
            }

        updated_rows.append(updated)

    write_csv(UNIVERSE_PATH, CSV_FIELD_ORDER, updated_rows)
    exclusion_rows = [generated_exclusions[key] for key in sorted(generated_exclusions)]
    write_csv(
        EXCLUSIONS_PATH,
        ["journal_id", "journal_name", "exclusion_reason", "evidence_basis", "date_excluded", "notes"],
        exclusion_rows,
    )

    print(f"Updated language fields for {len(updated_rows)} journals")
    print(f"Coded inclusion decisions: {coded_count}")
    print(f"Included in language-eligible population: {included_count}")
    print(f"Excluded from language-eligible population: {excluded_count}")


if __name__ == "__main__":
    main()
