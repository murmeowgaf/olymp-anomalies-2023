# Data Folder

This folder contains raw data used for the analysis.

## OPJU files
- Located in `/data/opju/`.
- Format: OriginLab `.opju` (proprietary).
- Purpose: raw histograms and score distributions from the 2023 Astronomy Olympiad.
- These files can be opened with OriginLab software or converted to CSV.

## CSV schema (planned)
We also provide an empty CSV template (`scores_2023_schema.csv`) that shows how 
aggregated counts can be stored for statistical testing.

Columns:
- `year` (int)
- `grade` (int) — 9 or 10
- `category` (str) — Blitz / Theory / Practical
- `task_id` (str) — e.g., T9.4, P9.7
- `region_group` (str) — MO / Rest
- `score` (int)
- `count` (int)

This allows reproducible χ² / Fisher / Mann–Whitney tests once raw bin counts are extracted.
