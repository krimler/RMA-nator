#!/usr/bin/env python3
# kpi_dir_summary.py — summarize all JSONL files in a directory
#python kpi_dir_summary.py ./rmanator_examples > summary.csv

import sys, glob, os
from kpi_reader import kpis

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python kpi_dir_summary.py <dir_with_jsonl>", file=sys.stderr)
        sys.exit(2)
    print("file,FR,TTR_med_h,RR")
    for path in sorted(glob.glob(os.path.join(sys.argv[1], "*.jsonl"))):
        fr, ttr, rr = kpis(path)
        print(f"{os.path.basename(path)},{fr:.3f},{ttr:.2f},{rr:.3f}")

