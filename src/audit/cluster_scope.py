def audit_cluster_scope(registry):
    violations = []
    for f in registry["features"]:
        if f.get("cluster_adjusted") not in ["N/A", None]:
            if f["unit_of_observation"] not in ["wallet", "holder", "cluster"]:
                violations.append(f["feature_id"])
    return violations