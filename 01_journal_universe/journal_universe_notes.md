# Journal Universe Notes

Use this file to document cleaning decisions, source ambiguities, ISSN reconciliation, and category judgment calls.

## 2026-05-19 PJIP import

- Source page: https://www.pjip.org/ranking-index.html
- Underlying data feed: https://www.pjip.org/uploads/1/4/8/0/148077507/custom_themes/727891833533859441/files/PJIP_data_JSON_008.txt
- Imported rows: 274
- Local extraction artifacts archived under `00_sources/pjip_extraction_artifacts/` with `payloads/`, `page_capture/`, and `tools/` subfolders.

## Field mapping

- `journal_name_raw` and `journal_name` were extracted from the HTML anchor in `Journal Name (Linked)`.
- `journal_url_raw` and `journal_url` were normalized to absolute `https://www.pjip.org/journal-profile.html?...` URLs.
- `publisher` came directly from the PJIP `Publisher` field.
- `issn_raw` and `issn_online` came from the PJIP `eISSN` field. `issn_print` remains blank pending separate verification.
- `category_raw` preserves the PJIP area code.

## Category normalization

- `GNRL` was mapped to `primary_category = generalist` and `secondary_category = generalist_philosophy`.
- All other PJIP area codes were mapped to `primary_category = specialist`.
- The specific subject area was preserved in `secondary_category` and again in `notes` as `pjip_area_code=...`.

## Provisional assumptions

- `peer_reviewed`, `active_status`, `publishes_research_articles`, and `included_in_sampling_frame` were set to `yes` or `active` for the imported frame so the sample script can operate on the universe.
- These fields should be audited and revised if you want a stricter inclusion screen before final sampling.

## Current sampling implication

- The current imported population contains two active `primary_category` strata for sampling: `generalist` (76 journals) and `specialist` (198 journals).
- Because the imported frame does not currently populate `interdisciplinary` or `applied` as separate `primary_category` values, the sampling configuration now uses proportional allocation across the two observed strata.

## Language eligibility audit

- Add and populate these fields in `journal_universe_clean.csv`: `language_status`, `primary_publication_language`, `english_policy_available`, `english_articles_available`, `language_exclusion_reason`, and `included_in_language_eligible_population`.
- Suggested `language_status` values: `english_primary`, `multilingual_english_available`, `non_english_primary`, `unclear`.
- Journals should only receive `included_in_language_eligible_population = yes` when they can be coded reliably for this study in English.
- Language-based exclusions should be logged transparently rather than silently omitted from the population.

## 2026-05-19 first-pass language audit results

- Source dataset: https://www.pjip.org/uploads/1/4/8/0/148077507/custom_themes/727891833533859441/files/z_en_Philosophy.json
- Audit script: `01_journal_universe/audit_language_eligibility.py`
- `language_status` distribution after normalization: `english_primary = 223`, `multilingual_english_available = 37`, `unclear = 14`
- `english_policy_available` distribution: `yes = 151`, `unclear = 123`
- `included_in_language_eligible_population` decisions: `yes = 150`, unresolved blank = `124`
- Current conservative analyzed population for sampling: `150`

This first-pass audit intentionally treats unresolved multilingual accessibility cases conservatively. Journals with clear English-primary publication status are included, non-English-primary journals are excluded, and journals requiring stronger evidence of English-accessible policy/article materials remain blank pending manual review.