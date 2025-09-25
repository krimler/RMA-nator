# RMA-nator

This repository accompanies the **experience report on RMA-nator**, a production system for
operating-through-failure link management at hyperscale.  
It contains a **minimal synthetic artifact** that lets readers regenerate figures and compute KPIs
without exposing production data.

---

## Contents

- **OpenRMA-Trace.md**  
  Minimal JSONL schema for candidate link event records.

- **gen.py**  
  Synthetic generator for OpenRMA traces. Produces JSONL files with fields
  needed to compute KPIs and ablations.

- **scorecard.py**  
  Utility functions to load JSONL traces and compute:
  - False RMA rate (FR)  
  - Median Time to Repair (TTR)  
  - Rescue Rate (RR)

- **make_reproduce.py**  
  Tiny reproducibility script that:
  1. Loads a JSONL trace
  2. Computes KPIs
  3. Generates a sample histogram of TTR as a **PDF at 600 dpi**

---

## Quick Start

1. **Clone this repository**
   ```bash
   git clone https://github.com/<your-org>/rmanator-experience-report.git
   cd rmanator-experience-report
   ```

2. **Generate synthetic data**
   ```bash
   python gen.py --out example.jsonl --n 200 --variant weekly
   ```

3. **Compute KPIs and make a figure**
   ```bash
   python make_reproduce.py
   ```

4. **Outputs**
   - `KPIs` printed to the console (FR, TTR median, RR)
   - `figures/ttr_hist.pdf` — histogram of TTR (synthetic)

---

## Schema (OpenRMA v0.1)

```json
{
  "incident_id": "uuid",
  "ts_open": "RFC3339",
  "site_bin": "region-agg",
  "link_class": "agg|core|wan|edge",
  "signals": { "crc": [...], "flaps": [...] },
  "forecaster": "prophet",
  "fusion_features": { "x1": 0.0, "x2": 0.0 },
  "decision": "retain|clean|rma",
  "ts_decision": "RFC3339",
  "ttr_hours": 0.0,
  "stability_window_days": 7,
  "reincident_within_window": false,
  "tuner_release": "YYYY-WW",
  "variant": "baseline|fixed|retuned|weekly",
  "false_rma_counterfactual": false
}
```

---

## Notes

- All data here are **synthetic** and generated locally.
- Figures are saved as **PDF at 600 dpi**.
- This artifact is **not** production code. It documents the schema,
  KPIs, and reproducibility path for the paper.

---

## License

Apache 2.0
