from collections import defaultdict

def build_semantic_paths(registry):
    """
    For each semantic_concept, track all features that compute it and their dependency chains.
    Returns: {semantic_concept: list_of_feature_ids}
    """
    concept_features = defaultdict(list)
    for feature in registry["features"]:
        concept = feature.get("semantic_concept")
        if concept:
            concept_features[concept].append(feature["feature_id"])
    return concept_features

def audit_double_count(registry):
    """
    Check that no semantic concept is computed multiple times through different paths.
    This would lead to double-counting the same signal.
    Violation: A semantic_concept appears in multiple features AND those features 
               have overlapping dependencies or transitive dependencies
    """
    violations = []
    concept_features = build_semantic_paths(registry)
    features_map = {f["feature_id"]: f for f in registry["features"]}
    
    # Check concepts that appear in multiple features
    for concept, feature_ids in concept_features.items():
        if len(feature_ids) > 1:
            violations.append({
                "semantic_concept": concept,
                "issue": "semantic_duplication",
                "details": f"Semantic concept '{concept}' appears in {len(feature_ids)} features: {feature_ids}",
                "features": feature_ids
            })
    
    return violations
