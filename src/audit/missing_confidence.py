def audit_missing_confidence(registry):
    """
    Check that features with critical roles have appropriate missing_data_rule.
    Violation: Features with primary_role in [Direction, Strength, Signal] have missing_data_rule='mark_unavailable',
               but missing confidence score is not properly propagated OR
               Features with primary_role=Confidence should never have mark_unavailable
    """
    violations = []
    features_map = {f["feature_id"]: f for f in registry["features"]}
    
    critical_roles = ["Direction", "Strength", "Signal"]
    confidence_roles = ["Confidence", "Quality"]
    
    for feature in registry["features"]:
        feature_id = feature["feature_id"]
        primary_role = feature.get("primary_role")
        missing_data_rule = feature.get("missing_data_rule")
        
        # Critical roles should use mark_unavailable for proper confidence propagation
        if primary_role in critical_roles:
            if missing_data_rule not in ["mark_unavailable", "drop"]:
                violations.append({
                    "feature_id": feature_id,
                    "issue": "missing_confidence_rule",
                    "details": f"Feature with primary_role='{primary_role}' should use mark_unavailable/drop but has '{missing_data_rule}'"
                })
        
        # Confidence/Quality features should never drop data silently
        if primary_role in confidence_roles:
            if missing_data_rule == "drop":
                violations.append({
                    "feature_id": feature_id,
                    "issue": "confidence_data_loss",
                    "details": f"Confidence feature '{feature_id}' should not silently drop missing data"
                })
    
    return violations
