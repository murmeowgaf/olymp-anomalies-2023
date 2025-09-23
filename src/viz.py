import pandas as pd
import matplotlib.pyplot as plt

def plot_overlaid_hist(df_bins, grade, task_id, outpath):
    d = df_bins[(df_bins['grade']==grade) & (df_bins['task_id']==task_id)]
    if d.empty:
        return
    if (d['mo_count'].sum() + d['rest_count'].sum()) == 0:
        return

    bins = d['score_bin'].astype(str).unique().tolist()
    mo = d.set_index('score_bin').reindex(bins)['mo_count'].fillna(0)
    rest = d.set_index('score_bin').reindex(bins)['rest_count'].fillna(0)

    plt.figure()
    x = range(len(bins))
    width = 0.4
    plt.bar([i - width/2 for i in x], mo.values, width, label='MO')
    plt.bar([i + width/2 for i in x], rest.values, width, label='Rest')
    plt.xticks(list(x), bins, rotation=45)
    plt.title(f"Grade {grade} — {task_id}: MO vs Rest (counts)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()
