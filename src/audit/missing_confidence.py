def audit_missing_confidence(registry):
    """
    Check that features with critical roles have appropriate missing_data_rule.
    Rules:
    - Direction/Strength/Signal roles → must use forward_fill (not mark_unavailable)
    - Quality/Confidence roles → mark_unavailable is allowed (for proper handling)
    - All roles → drop is allowed but not recommended
    """
    violations = []
    
    for feature in registry["features"]:
        feature_id = feature["feature_id"]
        primary_role = feature.get("primary_role")
        missing_data_rule = feature.get("missing_data_rule")
        
        # Only report violations if the rule-role combination is INVALID
        # Valid combinations:
        # - Direction/Strength/Signal with forward_fill → OK
        # - Quality/Confidence with mark_unavailable → OK
        # - Any role with drop → OK (allowed but not recommended)
        
        # Invalid: Direction/Strength/Signal with mark_unavailable
        if primary_role in ["Direction", "Strength", "Signal"]:
            if missing_data_rule == "mark_unavailable":
                violations.append({
                    "feature_id": feature_id,
                    "issue": "missing_confidence_rule_violation",
                    "details": f"Feature with primary_role='{primary_role}' cannot use mark_unavailable"
                })
    
    return violations
