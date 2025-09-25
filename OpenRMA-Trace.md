# OpenRMA Trace v0.1 (Specification)

This schema defines the minimal event record used by RMA-nator.

**Record (JSON Lines):**
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

**Notes:**
- `stability_window_days` is fixed at 7 for v1.0 Saved Link definition.
- `false_rma_counterfactual` is a conservative flag derived from shadow policies.
