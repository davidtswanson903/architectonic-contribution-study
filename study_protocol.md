# Study Protocol

Study title: Architectonic Contribution Audit in Philosophy Journals

Purpose: Build a transparent, replayable empirical archive for evaluating how philosophy journals invite, publish, and classify architectonic contributions.

Research questions:
- How do sampled journals publicly articulate contribution criteria, review transparency, scope openness, and policy opacity for standard and nonstandard philosophical work?
- How often do sampled articles make local, relational, architectonic, operational, interpretive, applied, or survey-like contributions in the target sense?
- How do observed rates vary by journal category, article type, and coding threshold?

Sampling frame: `01_journal_universe/journal_universe_clean.csv`

Analyzed population definition: English-language or English-accessible peer-reviewed philosophy journals listed in PJIP that publish ordinary research articles.

Inclusion criteria:
- Active journals
- English-primary journals, or multilingual journals with usable English policy pages and English-language research articles
- Peer-reviewed venues
- Publishes research articles
- Included in the sampling frame with an explicit rationale

Exclusion criteria:
- Inactive journals
- Non-English-primary journals that cannot be coded reliably in English
- Journals without usable English policy pages or English-language article materials for the audit
- Venues without research articles
- Journals excluded for documented methodological reasons

Sampling method: Proportional stratified random sampling by `primary_category`

Sampling parameters:
- Raw PJIP intake population: `N = 274`
- Current confirmed analyzed population for the journal-documentation audit: `N = 150` journals coded `included_in_language_eligible_population = yes`
- Unresolved language-accessibility cases remaining after the first-pass audit: `124`
- Confidence level: `95%`
- Assumed response distribution: `p = 0.5`
- Target margin of error: `+/-10%`
- Finite-population formula: `n = n0 / (1 + ((n0 - 1) / N))`, where `n0 = z^2 * p * (1 - p) / e^2`
- Current finite-population result for `N = 150`: `n0 = 96.04`, adjusted `n = 58.79`, rounded sample `n = 59`
- Allocation rule: proportional to the observed eligible population strata in `journal_universe_clean.csv`

Journal-documentation audit sample size: `59` journals from the confirmed language-eligible population, with unresolved journals held out pending manual review (`15` generalist, `44` specialist)

Random seed: 20260519

Sampling script: `02_sampling/sample_journals.py`

Target year or years: 2025

Journal categories:
- generalist
- specialist

Document types collected:
- aims_scope
- submission_guidelines
- author_instructions
- reviewer_guidelines
- editorial_policy
- desk_rejection_policy
- article_types
- review_essay_policy
- special_issue_policy
- ethics_policy
- other

Document collection and preservation:
- Record each collected journal document in `03_journal_documents/documents_index.csv`.
- Preserve a source snapshot where feasible, plus extracted text used for coding.
- When rendered content is difficult to preserve reliably, also preserve a full-page screenshot and a relevant excerpt screenshot.
- Use the controlled extraction-method vocabulary defined in `03_journal_documents/collection_policy.md`.
- Record extraction problems, manual extraction notes, collector identity, and per-artifact hashes for preserved source files.

Coding categories:
- Journal policy codes in `04_journal_policy_coding/policy_coding.csv`, including eligibility, documentation availability, review transparency, contribution criteria, architectonic recognition, scope openness, opacity, and derived reviewability profiles
- Article contribution codes in `06_article_coding/article_contribution_coding.csv`, including article eligibility, contribution function, scope level, architectonic strength, architecture-dependence, carrier form, operational direction, and derived sensitivity counts
- Evidence rows in the corresponding evidence files

Limitations:
- Coding remains interpretive even with preserved evidence excerpts.
- Sample quality depends on journal universe completeness and source quality.
- Findings will generalize to the English-language or English-accessible analyzed population, not automatically to all philosophy journals globally.
- Policy documents and article metadata may change after collection, so collection dates matter.