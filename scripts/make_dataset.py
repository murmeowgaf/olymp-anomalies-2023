#!/usr/bin/env python3
import argparse, json
from src.io_loaders import load_excel_three_sheets
from src.cleaning import clean_and_tidy

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--config', default='config.json')
    ap.add_argument('--out_interim', default='data/interim/scores_tidy.csv')
    args = ap.parse_args()

    cfg = json.load(open(args.config, 'r', encoding='utf-8'))
    df = load_excel_three_sheets(args.input, cfg['sheet_map'])
    tidy = clean_and_tidy(df, cfg['region_synonyms_mo'], cfg['task_prefix'], cfg['task_count'])
    tidy.to_csv(args.out_interim, index=False)
    print(f"Wrote {args.out_interim}, rows={len(tidy)}")

if __name__ == '__main__':
    main()
