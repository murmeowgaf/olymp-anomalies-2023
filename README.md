# olymp-anomalies-2023
# All-Russian Astronomy Olympiad (2023): Regional Anomalies
# Astronomy Olympiad Anomalies (2023)

Independent analysis of the **All-Russian Astronomy Olympiad 2023** (grades 9–10).  
We compare score distributions of the **Moscow Region (MO)** with other regions.

**Hypothesis:** Results from MO show consistent right-shifts and top-bin spikes,  
compatible with prior exposure to leaked tasks.

## Contents
- 📊 Graphs: `/data/graphs/`
- 📂 Raw OriginLab files: `/data/opju/`
- 📝 Report with methodology and findings: `REPORT.md`

## Key Observations
- MO participants systematically overrepresented in high-score bins.
- Distributions in multiple Theory, Practical, and Blitz tasks are skewed.
- Pattern repeats across grades 9 and 10, reducing likelihood of random chance.

## Example Graphs
![Blitz Example](graphs/blitz1.png)
![Theory Example](graphs/theor9-4.png)

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
