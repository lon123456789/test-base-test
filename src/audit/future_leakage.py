def audit_future_leakage(registry):
    violations = []
    for f in registry["features"]:
        if f.get("uses_future") is False:
            for parent in f.get("depends_on", []):
                p = next((x for x in registry["features"] if x["feature_id"] == parent), None)
                if p and p.get("uses_future") is True:
                    violations.append((f["feature_id"], parent))
    return violations