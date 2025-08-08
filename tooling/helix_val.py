#!/usr/bin/env python3
"""
helix_val.py — NBML validator (v0.2 reference)

Usage (locally):
  python tooling/helix_val.py validate path/to/file.yaml --json
  python tooling/helix_val.py score path/to/file.json --json
"""
import argparse, json, os

def _maybe_import_yaml():
    try:
        import yaml  # type: ignore
        return yaml
    except Exception:
        return None

def load_nbml(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext in [".yaml", ".yml"]:
        yaml = _maybe_import_yaml()
        if yaml is None:
            raise RuntimeError("PyYAML not installed. Use JSON or `pip install pyyaml`.")
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    elif ext == ".json":
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        raise RuntimeError("Unsupported file extension. Use .yaml/.yml or .json")

def check_structure(doc):
    version = doc.get("version")
    if version not in ("NBML-0.2", "NBML-0.1"):
        return False, [f"version must be 'NBML-0.2' (or 'NBML-0.1' for compatibility), got {version!r}"], [], 0.0
    beats = doc.get("beats", [])
    errors, warnings = [], []
    if not isinstance(beats, list) or not beats:
        return False, ["beats[] must be a non-empty array"], [], 0.0
    ids = set(); dupes = set(); missing = 0
    req = ["id", "label", "goal", "conflict", "stakes", "callbacks"]
    for b in beats:
        for k in req:
            v = b.get(k)
            if v is None or (isinstance(v, str) and not v.strip()):
                missing += 1
        bid = b.get("id")
        if bid in ids: dupes.add(bid)
        ids.add(bid)
    if dupes: errors.append(f"duplicate beat ids: {sorted(dupes)}")
    if missing: warnings.append(f"{missing} missing required fields across beats")
    score = max(0.0, 100.0 - (len(dupes)*15) - (missing*2))
    return (not dupes), errors, warnings, score

def check_callbacks(doc):
    beats = doc.get("beats", [])
    id_to_idx = {b.get("id"): i for i,b in enumerate(beats)}
    errors, warnings = [], []
    invalid = forward = 0
    for i,b in enumerate(beats):
        for ref in (b.get("callbacks") or []):
            if ref not in id_to_idx:
                invalid += 1; errors.append(f"{b.get('id')} -> missing callback '{ref}'")
            elif id_to_idx[ref] >= i:
                forward += 1; errors.append(f"{b.get('id')} -> forward callback to '{ref}'")
    score = max(0.0, 100.0 - invalid*10 - forward*8)
    return (invalid==0 and forward==0), errors, warnings, score

def check_arcs(doc):
    arcs = doc.get("arcs") or []
    beats = doc.get("beats") or []
    beat_ids = {b.get("id") for b in beats}
    errors, warnings = [], []
    invalid = nochange = 0
    for a in arcs:
        if a.get("start_trait") == a.get("end_trait"):
            nochange += 1; errors.append(f"arc {a.get('character')} has no change")
        for p in (a.get("pivot_beats") or []):
            if p not in beat_ids:
                invalid += 1; errors.append(f"arc {a.get('character')} references missing pivot '{p}'")
    score = max(0.0, 100.0 - invalid*10 - nochange*15)
    return (invalid==0 and nochange==0), errors, warnings, score

def check_progression(doc):
    beats = doc.get("beats", [])
    ok_ct = 0
    for b in beats:
        if all((b.get("goal","").strip(), b.get("conflict","").strip(), b.get("stakes","").strip())):
            ok_ct += 1
    ratio = ok_ct / max(1, len(beats))
    score = min(100.0, ratio*100.0)
    warnings = []
    if ratio < 0.7:
        warnings.append(f"only {int(ratio*100)}% of beats have goal+conflict+stakes")
    return ratio >= 0.7, [], warnings, score

STAKE_KW = ["or else","risk","cost","die","lose","deadline","exposure","consequence","irreversible","cannot","must"]

def check_stakes(doc):
    beats = doc.get("beats", [])
    growth = 0; prev_len = 0
    for b in beats:
        s = (b.get("stakes","") or "").lower()
        if any(kw in s for kw in STAKE_KW) or len(s) > prev_len:
            growth += 1
        prev_len = max(prev_len, len(s))
    ratio = growth / max(1, len(beats))
    score = min(100.0, ratio*100.0)
    warnings = []
    if ratio < 0.6:
        warnings.append("stakes may not escalate (heuristic)")
    return ratio >= 0.6, [], warnings, score

def check_min_beats(doc, minimum=8):
    beats = doc.get("beats", [])
    ok = len(beats) >= minimum
    score = 100.0 if ok else (len(beats)/max(1,minimum))*100.0
    return ok, ([] if ok else [f"requires at least {minimum} beats"]), [], score

CHECKS = [
    ("structure_score", check_structure, 1.0),
    ("callback_score", check_callbacks, 1.0),
    ("arc_score", check_arcs, 1.0),
    ("progression_score", check_progression, 1.0),
    ("stakes_score", check_stakes, 1.0),
    ("min_beats_score", check_min_beats, 1.0),
]

def evaluate(doc):
    results = {}; total = 0.0; weights = 0.0; errs_all=[]; warns_all=[]
    for name, fn, w in CHECKS:
        ok, errs, warns, score = fn(doc)
        results[name] = {"ok": ok, "score": round(score,1), "errors": errs, "warnings": warns}
        total += score*w; weights += w
        errs_all += errs; warns_all += warns
    results["total"] = round(total/weights if weights else 0.0, 1)
    results["errors"] = errs_all; results["warnings"] = warns_all
    return results

def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd")
    v = sp.add_parser("validate"); v.add_argument("path"); v.add_argument("--json", action="store_true")
    s = sp.add_parser("score"); s.add_argument("path"); s.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not args.cmd: ap.print_help(); return
    doc = load_nbml(args.path)
    res = evaluate(doc)
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(f"TOTAL: {res['total']}")
        for name, *_ in CHECKS:
            r = res[name]; status = "OK " if r["ok"] else "WARN"
            print(f"{status:<4} {name:<18} {r['score']:>5}")
        if res["errors"]:
            print("\nErrors:"); [print(f" - {e}") for e in res["errors"]]
        if res["warnings"]:
            print("\nWarnings:"); [print(f" - {w}") for w in res["warnings"]]
if __name__ == "__main__":
    main()
