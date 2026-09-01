from collections import defaultdict

def build_dag(registry):
    """
    Build DAG from registry features and edges.
    """
    dag = defaultdict(list)
    
    # Add edges from depends_on
    for feature in registry["features"]:
        for parent in feature.get("depends_on", []):
            dag[parent].append(feature["feature_id"])
    
    # Add explicit edges
    for edge in registry.get("edges", []):
        dag[edge["from"]].append(edge["to"])
    
    return dag

def has_path(dag, start, end, visited=None):
    """
    Check if there's a path from start to end in the DAG.
    """
    if visited is None:
        visited = set()
    if start in visited:
        return False
    if start == end:
        return True
    
    visited.add(start)
    for neighbor in dag.get(start, []):
        if has_path(dag, neighbor, end, visited.copy()):
            return True
    return False

def audit_illegal_feedback(registry):
    """
    Detect cycles in the DAG.
    A cycle is detected when there's a path from a node back to itself.
    Violation: Feature A depends on B, and B has a path back to A (direct or transitive)
    """
    violations = []
    dag = build_dag(registry)
    features_map = {f["feature_id"]: f for f in registry["features"]}
    
    # For each feature, check if there's a cycle
    for feature_id in dag:
        # Check if any child can reach back to this feature
        for child in dag.get(feature_id, []):
            if has_path(dag, child, feature_id):
                violations.append({
                    "feature_id": feature_id,
                    "issue": "cycle_detected",
                    "details": f"Feature {feature_id} has a path back to itself through {child}"
                })
                break  # Report once per cycle
    
    return violations
