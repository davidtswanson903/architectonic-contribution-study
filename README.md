# Architectonic Review Study

This repository is scaffolded as a replayable empirical archive for studying architectonic contributions in philosophy journals. The design separates preserved source material from catalogue records, coding layers, and integrity metadata.

## Structure

- `00_sources/`: external source registry and collection notes
- `01_journal_universe/`: raw and cleaned journal sampling frame
- `02_sampling/`: deterministic sampling config, script, sample output, and log
- `03_journal_documents/`: preserved journal policy documents, raw text captures, later extracted text, and collection policy
- `04_journal_policy_coding/`: journal-level policy coding for review transparency, contribution criteria, architectonic recognition, and opacity
- `05_article_catalogue/`: yearly article catalogue and notes
- `06_article_coding/`: article-level contribution-function coding, architectonic strength, and evidence
- `07_analysis/`: reproducible analysis scripts and generated outputs
- `08_paper_outputs/`: paper-facing tables, appendix material, and methods text
- `temp/`: temporary intake workspace for one-off or batch artifact ingestion before indexing

## Workflow

1. Populate `00_sources/source_registry.csv` with source lists used to construct the journal universe.
2. Preserve raw journal-universe intake in `01_journal_universe/journal_universe_raw.csv`.
3. Clean, justify, and exclude journals explicitly in the `01_journal_universe/` files.
4. Configure and run `02_sampling/sample_journals.py` to generate a replayable sample.
5. Run `03_journal_documents/generate_sample_artifact_folders.py` to create sample-based journal folders under `03_journal_documents/raw/` and `03_journal_documents/extracted_text/`.
6. Run `03_journal_documents/prepopulate_documents_index.py` to create starter document-index rows for each sampled journal and document type.
7. Follow `03_journal_documents/collection_policy.md` when preserving source snapshots, screenshots, and raw text captures for each journal document. Reserve `extracted_text/` for the later ontology-driven extraction stage.
8. Track every collected artifact in `03_journal_documents/documents_index.csv`.
9. Use `temp/journal_document_intake/record_journal_document_receipts.py` when you want to ingest one document or a small batch of artifacts from a temporary workspace into the canonical collection structure.
	Raw copied text should be ingested with `--raw-text`; the script still accepts `--extracted-text` as a temporary compatibility alias during the raw-receipt phase.
10. Code journal policy and article contribution layers while preserving evidence rows.
11. Run `07_analysis/analysis.py` to produce summary outputs.
12. Run `refresh_integrity.py` after substantive changes to refresh hashes and the manifest.

## Integrity

The repository includes a manifest and per-file `.sha256` files for the main research artifacts. Run `python .\refresh_integrity.py` after substantive changes so `manifest.csv`, the per-file sidecars, and the root manifest sidecars stay synchronized. Raw collected files should be appended to, never overwritten.

## Quick Start

```powershell
python .\02_sampling\sample_journals.py
python .\03_journal_documents\generate_sample_artifact_folders.py
python .\03_journal_documents\prepopulate_documents_index.py
python .\temp\journal_document_intake\record_journal_document_receipts.py --batch-csv .\temp\journal_document_intake\batch_template.csv --dry-run
python .\07_analysis\analysis.py
python .\refresh_integrity.py
```