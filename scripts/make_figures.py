#!/usr/bin/env python3
import argparse, os, pandas as pd
from src.viz import plot_overlaid_hist

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bins', default='data/processed/bins_mo_vs_rest_agg.csv')
    ap.add_argument('--outdir', default='reports/figures')
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    df = pd.read_csv(args.bins)
    for (g, t), _ in df.groupby(['grade','task_id']):
        out = os.path.join(args.outdir, f"grade{g}_{t}.png")
        plot_overlaid_hist(df, g, t, out)

if __name__ == '__main__':
    main()
