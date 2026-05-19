# Study Protocol

Study title: Architectonic Contribution Audit in Philosophy Journals

Purpose: Build a transparent, replayable empirical archive for evaluating how philosophy journals invite, publish, and classify architectonic contributions.

Research questions:
- How do sampled journals describe originality, novelty, debate entry, specialist legibility, and related publication expectations?
- How often do sampled articles make architectonic contributions in the target sense?
- How do observed rates vary by journal category, article type, and coding threshold?

Sampling frame: `01_journal_universe/journal_universe_clean.csv`

Inclusion criteria:
- Active journals
- Peer-reviewed venues
- Publishes research articles
- Included in the sampling frame with an explicit rationale

Exclusion criteria:
- Inactive journals
- Venues without research articles
- Journals excluded for documented methodological reasons

Sampling method: Stratified random sampling by `primary_category`

Random seed: 20260519

Sampling script: `02_sampling/sample_journals.py`

Target year or years: 2025

Journal categories:
- generalist
- interdisciplinary
- specialist
- applied

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

Coding categories:
- Journal policy codes in `04_journal_policy_coding/policy_coding.csv`
- Article contribution codes in `06_article_coding/article_contribution_coding.csv`
- Evidence rows in the corresponding evidence files

Limitations:
- Coding remains interpretive even with preserved evidence excerpts.
- Sample quality depends on journal universe completeness and source quality.
- Policy documents and article metadata may change after collection, so collection dates matter.