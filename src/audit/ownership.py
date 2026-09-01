def audit_ownership(registry):
    """
    Check that each semantic concept has a single owner_engine.
    Also verify that owner_engine and source_engine are compatible.
    Violation: Same semantic_concept owned by different engines OR
                owner_engine != source_engine when they should match
    """
    violations = []
    concept_ownership = {}  # {semantic_concept: owner_engine}
    
    for feature in registry["features"]:
        concept = feature.get("semantic_concept")
        owner = feature.get("owner_engine")
        source = feature.get("source_engine")
        
        if not concept or not owner:
            continue
        
        # Check ownership consistency
        if concept not in concept_ownership:
            concept_ownership[concept] = owner
        else:
            if concept_ownership[concept] != owner:
                violations.append({
                    "feature_id": feature["feature_id"],
                    "issue": "ownership_conflict",
                    "details": f"Semantic concept '{concept}' owned by both '{concept_ownership[concept]}' and '{owner}'"
                })
        
        # Check owner_engine matches source_engine
        if owner != source:
            violations.append({
                "feature_id": feature["feature_id"],
                "issue": "ownership_source_mismatch",
                "details": f"owner_engine='{owner}' but source_engine='{source}'"
            })
    
    return violations
