import streamlit as st
import pandas as pd

st.title('MO vs Rest — Per-task Explorer')
st.write('Load outputs produced by the pipeline and explore per-task differences.')

bins_path = st.text_input('Bins CSV', 'data/processed/bins_mo_vs_rest_agg.csv')
summary_path = st.text_input('Stats summary CSV', 'reports/stats_summary.csv')

try:
    bins_df = pd.read_csv(bins_path)
    tasks = sorted(bins_df['task_id'].unique().tolist())
    grades = sorted(bins_df['grade'].unique().tolist())
    t = st.selectbox('Task', tasks)
    g = st.selectbox('Grade', grades)
    sub = bins_df[(bins_df['task_id']==t) & (bins_df['grade']==g)]
    st.bar_chart(sub.set_index('score_bin')[['mo_count','rest_count']])
except Exception as e:
    st.info(f'Load data after running the pipeline. Error: {e}')

try:
    summary = pd.read_csv(summary_path)
    st.subheader('Significance (FDR=0.05)')
    st.dataframe(summary)
except Exception as e:
    st.info(f'Run stats to populate summary. Error: {e}')
