import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, fisher_exact, mannwhitneyu

def chi_or_fisher(row_counts: np.ndarray):
    """row_counts: 2 x k (MO first row, Rest second).
    Drop all-empty columns; return ('na', nan) if no usable data.
    Use Fisher for 2x2; chi2 otherwise.
    """
    row_counts = np.asarray(row_counts)
    if row_counts.ndim != 2 or row_counts.shape[0] != 2:
        return 'na', np.nan
    mask = ~((row_counts[0] == 0) & (row_counts[1] == 0))
    row_counts = row_counts[:, mask]
    if row_counts.size == 0 or row_counts.shape[1] == 0:
        return 'na', np.nan
    try:
        if row_counts.shape == (2, 2):
            _, p = fisher_exact(row_counts, alternative='two-sided')
            return 'fisher', p
        chi2, p, *_ = chi2_contingency(row_counts)
        return 'chi2', p
    except Exception:
        return 'na', np.nan

def mann_whitney_scores(scores_mo, scores_rest, alternative='greater'):
    scores_mo = np.asarray(scores_mo)
    scores_rest = np.asarray(scores_rest)
    if scores_mo.size < 3 or scores_rest.size < 3:
        return np.nan, np.nan
    try:
        u, p = mannwhitneyu(scores_mo, scores_rest, alternative=alternative)
        return u, p
    except Exception:
        return np.nan, np.nan

def fdr_bh(pvals, alpha=0.05):
    p = np.array(pvals, dtype=float)
    order = np.argsort(np.where(np.isnan(p), np.inf, p))
    ranked = p[order]
    n = len(p)
    thresh = alpha * (np.arange(1, n+1) / n)
    passed = ranked <= thresh
    if not np.any(passed):
        return np.zeros(n, dtype=bool), ranked, thresh
    k = np.max(np.where(passed))
    cutoff = ranked[k]
    return p <= cutoff, ranked, thresh
