def audit_missing_confidence(registry):
    """
    Check that features with critical roles have appropriate missing_data_rule.
    Rules:
    - Direction/Strength/Signal roles → must use forward_fill (not mark_unavailable)
    - Quality/Confidence roles → mark_unavailable is allowed (for proper handling)
    - All roles → drop is allowed but not recommended
    """
    violations = []
    features_map = {f["feature_id"]: f for f in registry["features"]}
    
    for feature in registry["features"]:
        feature_id = feature["feature_id"]
        primary_role = feature.get("primary_role")
        missing_data_rule = feature.get("missing_data_rule")
        
        # Direction/Strength/Signal should use forward_fill for continuity
        if primary_role in ["Direction", "Strength", "Signal"]:
            if missing_data_rule != "forward_fill":
                violations.append({
                    "feature_id": feature_id,
                    "issue": "missing_confidence_rule_violation",
                    "details": f"Feature with primary_role='{primary_role}' must use forward_fill but has '{missing_data_rule}'"
                })
        
        # Quality/Confidence roles can use mark_unavailable
        # (no violation for these)
    
    return violations
