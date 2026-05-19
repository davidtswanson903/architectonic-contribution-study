# Architectonic Review Study

This repository is scaffolded as a replayable empirical archive for studying architectonic contributions in philosophy journals. The design separates preserved source material from catalogue records, coding layers, and integrity metadata.

## Structure

- `00_sources/`: external source registry and collection notes
- `01_journal_universe/`: raw and cleaned journal sampling frame
- `02_sampling/`: deterministic sampling config, script, sample output, and log
- `03_journal_documents/`: preserved journal policy documents and extracted text
- `04_journal_policy_coding/`: journal-level policy coding and evidence links
- `05_article_catalogue/`: yearly article catalogue and notes
- `06_article_coding/`: article-level contribution coding and evidence
- `07_analysis/`: reproducible analysis scripts and generated outputs
- `08_paper_outputs/`: paper-facing tables, appendix material, and methods text

## Workflow

1. Populate `00_sources/source_registry.csv` with source lists used to construct the journal universe.
2. Preserve raw journal-universe intake in `01_journal_universe/journal_universe_raw.csv`.
3. Clean, justify, and exclude journals explicitly in the `01_journal_universe/` files.
4. Configure and run `02_sampling/sample_journals.py` to generate a replayable sample.
5. Preserve collected policy documents in `03_journal_documents/raw/` and track them in `documents_index.csv`.
6. Code journal policy and article contribution layers while preserving evidence rows.
7. Run `07_analysis/analysis.py` to produce summary outputs.
8. Refresh hashes and the manifest after substantive changes.

## Integrity

The repository includes a manifest and per-file `.sha256` files for the main research artifacts. Raw collected files should be appended to, never overwritten.

## Quick Start

```powershell
python .\02_sampling\sample_journals.py
python .\07_analysis\analysis.py
```