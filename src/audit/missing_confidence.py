def audit_missing_confidence(registry):
    """
    Check that features with critical roles have appropriate missing_data_rule.
    Only report violations when Direction/Strength/Signal use mark_unavailable.
    """
    violations = []
    
    for feature in registry["features"]:
        feature_id = feature["feature_id"]
        primary_role = feature.get("primary_role")
        missing_data_rule = feature.get("missing_data_rule")
        
        print(f"DEBUG: {feature_id} - role={primary_role}, rule={missing_data_rule}")
        
        # Invalid: Direction/Strength/Signal with mark_unavailable
        if primary_role in ["Direction", "Strength", "Signal"]:
            if missing_data_rule == "mark_unavailable":
                print(f"  -> VIOLATION: {feature_id} uses mark_unavailable")
                violations.append({
                    "feature_id": feature_id,
                    "issue": "missing_confidence_rule_violation",
                    "details": f"Feature with primary_role='{primary_role}' cannot use mark_unavailable"
                })
            else:
                print(f"  -> OK: {feature_id} uses {missing_data_rule}")
    
    print(f"FINAL VIOLATIONS: {len(violations)}")
    return violations
