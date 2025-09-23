import pandas as pd
from typing import Sequence

def bin_counts(tidy: pd.DataFrame, bin_edges: Sequence[float]) -> pd.DataFrame:
    tidy = tidy.copy()
    tidy['bin'] = pd.cut(tidy['score'], bins=bin_edges, right=True, include_lowest=True)
    g = tidy.groupby(['grade','task_id','bin','region_group'], observed=False).size().unstack(fill_value=0).reset_index()
    g.rename(columns={'MO':'mo_count','Rest':'rest_count'}, inplace=True)
    if 'mo_count' not in g.columns: g['mo_count']=0
    if 'rest_count' not in g.columns: g['rest_count']=0
    g['score_bin'] = g['bin'].astype(str)
    return g[['grade','task_id','score_bin','mo_count','rest_count']]
