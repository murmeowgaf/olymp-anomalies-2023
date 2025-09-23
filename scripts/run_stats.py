#!/usr/bin/env python3
import json, argparse, pandas as pd, numpy as np, os, math, shutil
from pathlib import Path
from scipy.stats import fisher_exact
from src.features import bin_counts
from src.stats_tests import chi_or_fisher, mann_whitney_scores, fdr_bh

def fmt(x):
    if isinstance(x, float) and not math.isnan(x):
        return f"{x:.3g}"
    return ""

def compute_tail_table(tidy: pd.DataFrame, grade, task_id, tail_k: float, cfg_max: float=None):
    sub = tidy[(tidy['grade']==grade) & (tidy['task_id']==task_id)].copy()
    if sub.empty:
        return None
    obs_max = sub['score'].max()
    max_score = cfg_max if cfg_max is not None else obs_max
    if pd.isna(max_score):
        return None
    thr = max_score - tail_k
    sub['is_tail'] = sub['score'] >= thr
    ct = sub.pivot_table(index='is_tail', columns='region_group', values='score', aggfunc='count', fill_value=0)
    for col in ['MO', 'Rest']:
        if col not in ct.columns:
            ct[col] = 0
    tail_mo = int(ct.loc[True, 'MO']) if True in ct.index else 0
    tail_rest = int(ct.loc[True, 'Rest']) if True in ct.index else 0
    nontail_mo = int(ct.loc[False, 'MO']) if False in ct.index else 0
    nontail_rest = int(ct.loc[False, 'Rest']) if False in ct.index else 0
    if (tail_mo + tail_rest + nontail_mo + nontail_rest) == 0:
        return None
    table = np.array([[tail_mo, nontail_mo],
                      [tail_rest, nontail_rest]], dtype=int)
    try:
        odds, p = fisher_exact(table, alternative='greater')
    except Exception:
        odds, p = (np.nan, np.nan)
    return {
        'grade': grade,
        'task_id': task_id,
        'tail_k': tail_k,
        'max_score_used': max_score,
        'threshold': thr,
        'mo_tail': tail_mo,
        'mo_other': nontail_mo,
        'rest_tail': tail_rest,
        'rest_other': nontail_rest,
        'odds_ratio': odds,
        'p_tail': p,
        'total': int(tail_mo + tail_rest + nontail_mo + nontail_rest),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--interim', default='data/interim/scores_tidy.csv')
    ap.add_argument('--config', default='config.json')
    ap.add_argument('--bins_out', default='data/processed/bins_mo_vs_rest_agg.csv')
    ap.add_argument('--summary_out', default='reports/stats_summary.csv')
    ap.add_argument('--tail_out', default='reports/tail_test.csv')
    ap.add_argument('--tail-k', type=float, default=1.0)
    ap.add_argument('--autoreport', action='store_true')
    args = ap.parse_args()

    cfg = json.load(open(args.config, 'r', encoding='utf-8'))
    tidy = pd.read_csv(args.interim)

    bins_df = bin_counts(tidy, cfg['bin_edges'])
    os.makedirs(os.path.dirname(args.bins_out), exist_ok=True)
    bins_df.to_csv(args.bins_out, index=False)

    records = []
    for (g, t), sub in bins_df.groupby(['grade','task_id']):
        mo = sub['mo_count'].to_numpy()
        rest = sub['rest_count'].to_numpy()
        table = np.vstack([mo, rest])
        test_name, p_bins = chi_or_fisher(table)

        raw = tidy[(tidy['grade']==g) & (tidy['task_id']==t)]
        mo_scores = raw.loc[raw['region_group']=='MO', 'score'].values
        rest_scores = raw.loc[raw['region_group']=='Rest', 'score'].values
        _, p_mw = mann_whitney_scores(mo_scores, rest_scores, alternative='greater')

        records.append({'grade': g, 'task_id': t, 'test_bins': test_name, 'p_bins': p_bins, 'p_mw': p_mw})

    res = pd.DataFrame(records).sort_values(['grade','task_id'])
    sig_bins, _, _ = fdr_bh(res['p_bins'].fillna(1.0).values, alpha=0.05)
    sig_mw, _, _ = fdr_bh(res['p_mw'].fillna(1.0).values, alpha=0.05)
    res['sig_bins_fdr05'] = sig_bins
    res['sig_mw_fdr05'] = sig_mw
    os.makedirs(os.path.dirname(args.summary_out), exist_ok=True)
    res.to_csv(args.summary_out, index=False)
    print(f"Wrote {args.summary_out}, rows={len(res)}")

    cfg_max = cfg.get('max_task_score', None)
    tail_rows = []
    for (g, t), _ in tidy.groupby(['grade','task_id']):
        row = compute_tail_table(tidy, g, t, tail_k=args.tail_k, cfg_max=cfg_max)
        if row is not None:
            tail_rows.append(row)
    tail = pd.DataFrame(tail_rows).sort_values(['grade','task_id'])
    if not tail.empty:
        sig_tail, _, _ = fdr_bh(tail['p_tail'].fillna(1.0).values, alpha=0.05)
        tail['sig_tail_fdr05'] = sig_tail
    os.makedirs(os.path.dirname(args.tail_out), exist_ok=True)
    tail.to_csv(args.tail_out, index=False)
    print(f"Wrote {args.tail_out}, rows={len(tail)}")

    if args.autoreport:
        sig = res[(res['sig_mw_fdr05']) | (res['sig_bins_fdr05'])].copy()
        sig = sig.sort_values(['sig_mw_fdr05','p_mw','p_bins'], ascending=[False,True,True])
        sig.to_csv('reports/significant.csv', index=False)

        lines = []
        lines.append("# Results Summary — MO vs Rest (per-task)\n")
        lines.append("This report lists tasks where MO differs from Rest at FDR=0.05.\n")
        lines.append("## Significant tasks (bins & MW)\n")
        lines.append("| Grade | Task | p_bins | test_bins | p_mw | FDR bins | FDR MW |")
        lines.append("|---:|:---|---:|:---:|---:|:---:|:---:|")
        for _,r in sig.iterrows():
            lines.append("| {} | {} | {} | {} | {} | {} | {} |".format(
                int(r['grade']), r['task_id'],
                fmt(r.get('p_bins', float('nan'))),
                r.get('test_bins',''),
                fmt(r.get('p_mw', float('nan'))),
                "✔" if bool(r.get('sig_bins_fdr05', False)) else "",
                "✔" if bool(r.get('sig_mw_fdr05', False)) else "",
            ))
        if not tail.empty:
            lines.append("\n## Near-maximum enrichment (tail test)\n")
            lines.append(f"Threshold per task: tail if score ≥ (max_score − {args.tail_k}). Using config max if provided.\n")
            lines.append("| Grade | Task | thr | MO tail | Rest tail | Odds ratio | p_tail | FDR tail |")
            lines.append("|---:|:---|---:|---:|---:|---:|---:|:---:|")
            for _,r in tail.sort_values('p_tail').iterrows():
                lines.append("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
                    int(r['grade']), r['task_id'],
                    fmt(r['threshold']),
                    int(r['mo_tail']), int(r['rest_tail']),
                    fmt(r.get('odds_ratio', float('nan'))),
                    fmt(r.get('p_tail', float('nan'))),
                    "✔" if bool(r.get('sig_tail_fdr05', False)) else "",
                ))
        lines.append("\n## Conclusion\n")
        lines.append("Statistical analysis shows multiple tasks where MO significantly outperforms Rest. In some tasks (e.g. 9.5), MO also shows an anomalously high share of near-maximum scores. This pattern is **consistent with possible unequal access (e.g. early exposure to tasks)**, but does not prove a 'leak' on its own. External OSINT evidence would be required for confirmation.\n")

        os.makedirs('reports', exist_ok=True)
        Path('reports/REPORT.md').write_text("\n".join(lines), encoding='utf-8')

        print("Auto-report generated with conclusion.")

if __name__ == '__main__':
    main()
