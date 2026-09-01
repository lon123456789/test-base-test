def audit_missing_confidence(registry):
    """
    Validate missing_data_rule for critical feature roles.
    Rules:
    - Direction / Strength / Signal → MUST use forward_fill
    - Quality / Confidence → mark_unavailable is allowed
    - drop is allowed for all roles
    """
    violations = []

    for feature in registry["features"]:
        feature_id = feature["feature_id"]
        primary_role = feature.get("primary_role")
        missing_data_rule = feature.get("missing_data_rule")

        # Direction / Strength / Signal → must NOT use mark_unavailable
        if primary_role in ["Direction", "Strength", "Signal"]:
            if missing_data_rule == "mark_unavailable":
                violations.append({
                    "feature_id": feature_id,
                    "issue": "missing_confidence_rule_violation",
                    "details": f"{feature_id} with role {primary_role} must use forward_fill, not mark_unavailable"
                })

        # Quality / Confidence → mark_unavailable is allowed
        # No violation needed

        # drop is allowed for all roles

    return violations
