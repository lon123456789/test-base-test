def audit_missing_confidence(registry):
    violations = []
    for f in registry["features"]:
        if f.get("missing_data_rule") == "mark_unavailable":
            if f.get("primary_role") in ["Direction", "Strength"]:
                violations.append(f["feature_id"])
    return violations