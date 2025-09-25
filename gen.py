# Synthetic generator for OpenRMA traces
import json, uuid, math
from datetime import datetime, timedelta
import numpy as np

targets = {
    "baseline": dict(fr=0.25, ttr_improve=0.0, saved=0.20),
    "fixed":    dict(fr=0.20, ttr_improve=0.10, saved=0.30),
    "retuned":  dict(fr=0.18, ttr_improve=0.15, saved=0.35),
    "weekly":   dict(fr=0.14, ttr_improve=0.27, saved=0.45)
}

def signals(T=24, lam_crc=0.6, lam_flap=0.2, rng=None):
    crc = rng.poisson(lam=lam_crc, size=T).tolist()
    flaps = rng.poisson(lam=lam_flap, size=T).tolist()
    return {"crc": crc, "flaps": flaps}

def ttr(base_hours, improve_frac, rng):
    mu = math.log(max(1e-3, base_hours*(1.0-improve_frac)))
    sigma = 0.3
    return float(np.clip(rng.lognormal(mean=mu, sigma=sigma), 0.25, 72.0))

def generate_profile(n_events=100, profile="mixed", variant="weekly", seed=123):
    rng = np.random.default_rng(seed)
    t0 = datetime.fromisoformat("2025-01-01T00:00:00+00:00")
    tgt = targets[variant]
    rows = []
    for i in range(n_events):
        ts_open = t0 + timedelta(hours=int(i % 240))
        decision = rng.choice(["retain","clean","rma"],
                              p={"baseline":[0.20,0.25,0.55],
                                 "fixed":[0.30,0.30,0.40],
                                 "retuned":[0.35,0.30,0.35],
                                 "weekly":[0.45,0.30,0.25]}[variant])
        rec = {
          "incident_id": str(uuid.uuid4()),
          "ts_open": ts_open.isoformat().replace("+00:00","Z"),
          "site_bin": f"r{int(rng.integers(1,6))}",
          "link_class": rng.choice(["agg","core","wan","edge"]),
          "signals": signals(rng=rng),
          "forecaster": "prophet",
          "fusion_features": {"x1": float(rng.normal()), "x2": float(rng.normal())},
          "decision": decision,
          "ts_decision": (ts_open+timedelta(hours=1)).isoformat().replace("+00:00","Z"),
          "ttr_hours": ttr(10.0, tgt["ttr_improve"], rng),
          "stability_window_days": 7,
          "reincident_within_window": bool(rng.random()>0.75),
          "tuner_release": "2025-W{:02d}".format(1 + (i//200)%52),
          "variant": variant,
          "false_rma_counterfactual": bool(rng.random() < tgt["fr"]) if decision=="rma" else False
        }
        rows.append(rec)
    return rows

if __name__=="__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, required=True)
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--profile", type=str, default="mixed")
    ap.add_argument("--variant", type=str, default="weekly")
    args = ap.parse_args()
    data = generate_profile(n_events=args.n, profile=args.profile, variant=args.variant)
    with open(args.out,"w") as f:
        for r in data: f.write(json.dumps(r)+"\n")
    print(f"Wrote {args.out}")
