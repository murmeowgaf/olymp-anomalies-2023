# 2023 Astronomy Olympiad — MO vs Rest: Analysis Plan & Findings

## Scope
- Year: 2023
- Grades: 9, 10
- Categories: Blitz, Theory, Practical
- Groups: **MO (Moscow Region)** vs **Other regions (Rest)**

## Visual findings (from `/graphs`)
**Grade 9**
- *Theory 9.4–9.6* (`theor9-4.png`, `theor9-5.png`, `theor9-6.png`): MO histograms are right-shifted with clear top-bin spikes; Rest shows flatter / more spread distributions.
- *Practical 9.7–9.8* (`prak9-7.png`, `prak9-8.png`): MO mass is concentrated in 11–15; Rest has more mass in mid-bins.
- Blitz overlays (`blitz1.png`, `blitz2.png`): several BL items have higher MO counts near top with depressed low bins.

**Grade 10**
- *Theory 10.1* (`theor10-1.png`): MO shows a tall peak around 5 and a secondary cluster near top (9–10); Rest is broader.
- *Theory 10.2–10.6* (`theor10-2.png` … `theor10-6.png`): repeated MO over-representation in high bins; depleted low bins.
- *Practical 10.7/10.8* (`praktheor10-7.png`, `prak10-8.png`, `prak-10-8-1.png`): MO density shifted to 11–15 with visible top spikes.

**Pattern:** the **same direction of deviation** appears across multiple independent tasks → unlikely under the null that MO and Rest are identically distributed.

## Statistical plan (once bin counts are added)
We treat per-task scores as **ordinal discrete**. For each task:

1. **Binned χ² test**  
   - H0: MO and Rest have the same distribution across score bins.  
   - Input: counts per score in MO and in Rest.  
   - Output: χ², df, *p*.

2. **Tail enrichment (near-perfect)**  
   - Define *T* = {max, max−1}.  
   - 2×2 table: Group × {Tail vs Non-tail}.  
   - Tests: Fisher’s exact; report **risk ratio (RR)** with CI; **Cohen’s h** as effect size.

3. **Ordinal shift**  
   - Mann–Whitney *U* (or Cliff’s *δ*).  
   - H0: same central tendency; report *U*, *p*, **δ**.

4. **Multiple-testing**  
   - Benjamini–Hochberg across all tasks in a grade/category.  
   - Flag tasks with FDR-adjusted *q* < 0.05.

5. **Robustness checks**  
   - Collapse sparse bins to keep expected counts ≥ 5 for χ².  
   - Sensitivity: tail defined as {max}, {max,max−1}, {top 10%}.

### Minimal CSV format
See `/data/scores_2023_schema.csv` and `/data/bins_mo_vs_rest_agg.csv`.

## Interim conclusion (based on visuals)
- Multiple tasks in both grades show **consistent MO right-shifts** and **top-bin spikes** absent in other regions.
- The pattern is **broad (many items)** and **directionally consistent**, which reduces the likelihood of random fluctuation.
- Pending quantitative tests on published counts, the evidence is **compatible with prior task exposure** in MO.

> This is an OSINT-style statistical screening; final claims require the raw counts per bin and pre-registered thresholds.
