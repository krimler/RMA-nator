#!/usr/bin/env python3
# kpi_reader.py — compute FR, median TTR, RR from one OpenRMA v0.1 JSONL file
#e.g. python kpi_reader.py mixed_weekly.jsonl
# FR=0.136  TTR_med=7.22h  RR=0.580

import json, statistics, sys

def kpis(jsonl_path):
    n = rma = fr_bad = saved = 0
    ttrs = []
    with open(jsonl_path, "r") as f:
        for line in f:
            r = json.loads(line)
            n += 1
            # median TTR
            if "ttr_hours" in r:
                ttrs.append(float(r["ttr_hours"]))
            # False-RMA rate = fraction of RMAs flagged avoidable by counterfactual
            if r.get("decision") == "rma":
                rma += 1
                if r.get("false_rma_counterfactual", False):
                    fr_bad += 1
            # Rescue rate = saved among all candidates (retain/clean & stable for 7 days)
            if r.get("decision") in ("retain", "clean") and not r.get("reincident_within_window", True):
                saved += 1
    fr = (fr_bad / rma) if rma else 0.0
    ttr_med = statistics.median(ttrs) if ttrs else float("nan")
    rr = (saved / n) if n else 0.0
    return fr, ttr_med, rr

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python kpi_reader.py <path/to/file.jsonl>", file=sys.stderr)
        sys.exit(2)
    fr, ttr, rr = kpis(sys.argv[1])
    print(f"FR={fr:.3f}  TTR_med={ttr:.2f}h  RR={rr:.3f}")

