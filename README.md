# olymp-anomalies-2023
# All-Russian Astronomy Olympiad (2023): Regional Anomalies
Independent analysis of the 2023 All-Russian Astronomy Olympiad results.
Score distributions for Moscow Region vs other regions show systematic anomalies
consistent with prior task exposure (leakage).

This repo documents a small independent study of the **2023 All-Russian Astronomy Olympiad**.
We compare score distributions of the **Moscow Region (MO)** vs **the rest of Russia** for Blitz, Theory, and Practical tasks (grades 9 and 10).

**Hypothesis.** MO distributions show systematic right-shifts / top-bin spikes consistent with **prior task exposure (leakage)**.

- 📊 Graphs: see `/graphs`.
- 🧪 Methods & stats plan: see `2023_astronomy_analysis.md`.
- 🧾 Data schema: see `/data/README_data.md`.

> Evidence is based on open sources and educational results; no personal data used. Findings are indicative (not a legal conclusion).

## Headline observations (visual)
Across multiple 2023 tasks, MO shows:
- **Top-heavy distributions** (higher share of max/near-max scores) vs other regions.
- **Suppressed low bins** + **peaks at top bins** repeating across tasks.
- **Consistency across categories**: Blitz, several Theory items, and Practical.

Examples (see images):
- `theor9-4.png`, `theor9-5.png`, `theor9-6.png` — repeated right-shift / top spikes in MO.
- `prak9-7.png`, `prak9-8.png` — MO mass concentrated at higher totals.
- `theor10-1.png` & `practical10-7.png` — MO peak near top with depleted lower bins.
- `blitz1.png`, `blitz2.png` — MO vs Regions patterns diverge across many BL items.

## What’s next
To make this **statistically tight**, we aggregate counts per score bin and run:
- χ² goodness-of-fit (binned), KS / Mann–Whitney for ordinal scores,
- tail-enrichment tests for **max / (max−1)** bins (Fisher’s exact, risk ratio),
- multiple-testing control (Benjamini–Hochberg), and effect sizes (Cohen’s *h*, Cliff’s *δ*).

When raw counts are added into `/data/bins_mo_vs_rest_agg.csv`, the notebook (TBD) reproduces the p-values and plots.
