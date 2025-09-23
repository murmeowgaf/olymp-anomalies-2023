# MO vs Rest — OSINT analysis (astronomy olympiad 2023)

**Goal:** Reproducible, transparent OSINT-style analysis comparing **Moscow Oblast (MO)** vs **Rest of regions** on per-task scores.

## TL;DR (2 minutes)
1. Put your Excel file with **3 sheets (9/10/11)** into `data/raw/`. Example name: `vsos2023-stat.xlsx`.
2. Install deps:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the pipeline end-to-end:
   ```bash
   python scripts/make_dataset.py --input data/raw/vsos2023-stat.xlsx
   python scripts/run_stats.py
   python scripts/make_figures.py
   ```
4. (Optional) Launch interactive demo:
   ```bash
   streamlit run app/app.py
   ```

## What this repo does
- **Loads** your Excel (3 sheets) or CSVs, cleans regions, maps to `MO` vs `Rest`.
- **Builds per-task distributions** with fixed bins.
- **Runs statistical tests** (chi-square/Fisher, Mann–Whitney, FDR correction).
- **Exports figures** and a **stats summary** ready for your hackathon portfolio.
- **Provenance & ethics** docs to fit OSINT expectations.

### Expected columns (flexible but recommended)
- `region` (raw region name), `grade` (9/10/11), task columns like `task1`, `task2`, ..., or a wide table per grade.
- If your sheet names differ, adjust `config.json`.

## Files you touch
- **`data/raw/vsos2023-stat.xlsx`** — your source file (3 sheets).
- **`config.json`** — sheet names, region synonyms, task pattern.

## Outputs
- `data/interim/scores_tidy.csv`
- `data/processed/bins_mo_vs_rest_agg.csv`
- `reports/stats_summary.csv`
- `reports/figures/*.png`

## One-sentence pitch
> Reproducible OSINT-grade analysis of olympiad task performance: MO vs Rest — per-task distributions, rigorous stats, clean provenance.

---

### Portfolio checkboxes
- ✅ Reproducible pipeline (scripts + modules)
- ✅ CI-ready (pytest stubs)
- ✅ OSINT provenance & ethics docs
- ✅ Figures + single-page summary
- ✅ Optional interactive demo (Streamlit)
