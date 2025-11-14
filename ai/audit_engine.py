import json, datetime, pathlib
LOG_DIR = pathlib.Path("ai/audit_logs"); LOG_DIR.mkdir(exist_ok=True, parents=True)
def write_audit(module, changes, plan, risks):
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    out = {"timestamp": ts, "module": module, "changes": changes, "plan": plan, "risks": risks}
    (LOG_DIR / f"{ts}.json").write_text(json.dumps(out, indent=2))
    return f"{ts}.json"
