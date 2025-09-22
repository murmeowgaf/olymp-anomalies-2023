import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, fisher_exact, mannwhitneyu

df = pd.read_csv("data/bins_mo_vs_rest_agg.csv")

def chi_square_test(task_id):
    sub = df[df['task_id'] == task_id]
    table = np.vstack([sub['mo_count'].values, sub['rest_count'].values])
    chi2, p, dof, _ = chi2_contingency(table)
    return chi2, p

def fisher_tail_test(task_id):
    sub = df[df['task_id'] == task_id]
    max_score = sub['score'].max()
    tail = sub[sub['score'] >= max_score-1][['mo_count','rest_count']].sum()
    non  = sub[sub['score'] < max_score-1][['mo_count','rest_count']].sum()
    table = [[int(tail.mo_count), int(tail.rest_count)],
             [int(non.mo_count),  int(non.rest_count)]]
    odds, p = fisher_exact(table, alternative="greater")
    return odds, p

def mann_whitney_test(task_id):
    sub = df[df['task_id'] == task_id]
    mo_scores = np.repeat(sub['score'].values, sub['mo_count'].values)
    rest_scores = np.repeat(sub['score'].values, sub['rest_count'].values)
    u, p = mannwhitneyu(mo_scores, rest_scores, alternative="greater")
    return u, p
