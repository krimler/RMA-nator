# Reproduce synthetic figures and tables
import matplotlib.pyplot as plt, pandas as pd, numpy as np
from pathlib import Path
from scorecard import load_jsonl, kpis

def main():
    df = load_jsonl("example.jsonl")
    k = kpis(df)
    print("KPIs:",k)
    # simple plot
    plt.figure()
    plt.hist(df["ttr_hours"], bins=20)
    plt.xlabel("TTR (hours)"); plt.ylabel("count")
    plt.title("Distribution of TTR (synthetic)")
    plt.tight_layout()
    Path("figures").mkdir(exist_ok=True)
    plt.savefig("figures/ttr_hist.pdf", format="pdf", dpi=600)

if __name__=="__main__":
    main()
