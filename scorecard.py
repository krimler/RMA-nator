# KPI and survival utilities
import json, pandas as pd, numpy as np

def load_jsonl(path):
    rows = []
    with open(path) as f:
        for line in f:
            rows.append(json.loads(line))
    return pd.DataFrame(rows)

def kpis(df):
    rma_df = df[df["decision"]=="rma"]
    fr = (rma_df["false_rma_counterfactual"].sum() / max(1,len(rma_df))) if len(rma_df)>0 else 0.0
    ttr_med = float(df["ttr_hours"].median()) if "ttr_hours" in df else float("nan")
    saved = ((df["decision"].isin(["retain","clean"])) & (~df["reincident_within_window"])).sum()
    rr = saved / max(1,len(df))
    return dict(false_rma_rate=fr, ttr_median=ttr_med, rescue_rate=rr)
