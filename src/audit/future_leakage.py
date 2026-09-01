import json
from collections import defaultdict, deque

def build_upstream_closure(registry):
    """
    Build complete upstream dependency closure for each feature.
    Returns: {feature_id: set(all_upstream_features)}
    """
    features_map = {f["feature_id"]: f for f in registry["features"]}
    upstream_closure = defaultdict(set)
    
    def dfs_upstream(feature_id, visited=None):
        if visited is None:
            visited = set()
        if feature_id in visited:
            return set()
        visited.add(feature_id)
        
        feature = features_map.get(feature_id)
        if not feature:
            return set()
        
        upstream = set()
        for dep in feature.get("depends_on", []):
            upstream.add(dep)
            upstream.update(dfs_upstream(dep, visited))
        return upstream
    
    for feature_id in features_map:
        upstream_closure[feature_id] = dfs_upstream(feature_id)
    
    return upstream_closure

def audit_future_leakage(registry):
    """
    Check that no feature using present data depends on features using future data.
    Violation: A feature with uses_future=false has upstream dependency on uses_future=true
    """
    violations = []
    features_map = {f["feature_id"]: f for f in registry["features"]}
    upstream_closure = build_upstream_closure(registry)
    
    for feature in registry["features"]:
        # Only check features that explicitly use present data
        if feature.get("uses_future") is False:
            upstream_features = upstream_closure.get(feature["feature_id"], set())
            
            # Check if any upstream feature uses future data
            for upstream_id in upstream_features:
                upstream_feature = features_map.get(upstream_id)
                if upstream_feature and upstream_feature.get("uses_future") is True:
                    violations.append({
                        "feature_id": feature["feature_id"],
                        "issue": "future_leakage",
                        "details": f"Feature with uses_future=false depends (transitively) on {upstream_id} with uses_future=true"
                    })
                    break  # Report once per feature
    
    return violations
