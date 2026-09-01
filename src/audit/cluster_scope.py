def audit_cluster_scope(registry):
    """
    Check that features with cluster-adjusted properties only depend on cluster-compatible features.
    Violation: A feature with cluster_adjusted='yes' depends on non-cluster features, or
               a cluster-scoped feature (unit_of_observation='cluster') depends on holder-scoped features
    """
    violations = []
    features_map = {f["feature_id"]: f for f in registry["features"]}
    
    for feature in registry["features"]:
        feature_id = feature["feature_id"]
        unit_of_obs = feature.get("unit_of_observation")
        cluster_adjusted = feature.get("cluster_adjusted")
        
        # Check cluster-adjusted features
        if cluster_adjusted == "yes":
            for dep_id in feature.get("depends_on", []):
                dep_feature = features_map.get(dep_id)
                if not dep_feature:
                    continue
                dep_unit = dep_feature.get("unit_of_observation")
                # Cluster-adjusted features should depend on cluster or wallet scoped features
                if dep_unit not in ["cluster", "wallet", "holder"]:
                    violations.append({
                        "feature_id": feature_id,
                        "issue": "cluster_scope_violation",
                        "details": f"Cluster-adjusted feature depends on {dep_id} with unit_of_observation='{dep_unit}'"
                    })
        
        # Check cluster-scoped features
        if unit_of_obs == "cluster":
            for dep_id in feature.get("depends_on", []):
                dep_feature = features_map.get(dep_id)
                if not dep_feature:
                    continue
                dep_unit = dep_feature.get("unit_of_observation")
                # Cluster-scoped features should primarily depend on other cluster-scoped features
                if dep_unit == "holder":
                    # This is a warning level violation - allowed but should be noted
                    violations.append({
                        "feature_id": feature_id,
                        "issue": "cluster_scope_cross_level",
                        "details": f"Cluster-scoped feature depends on holder-scoped {dep_id}",
                        "severity": "warning"
                    })
    
    return violations
