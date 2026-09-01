from collections import defaultdict, deque

def detect_cycles(registry):
    """
    Detect cycles in the feature dependency graph using DFS.
    Returns list of features that are part of cycles.
    """
    # Build adjacency list from registry
    graph = defaultdict(list)
    all_nodes = set()
    
    for feature in registry.get("features", []):
        feature_id = feature["feature_id"]
        all_nodes.add(feature_id)
        
        # Add edges from depends_on
        for dep in feature.get("depends_on", []):
            graph[dep].append(feature_id)
            all_nodes.add(dep)
    
    # Add explicit edges
    for edge in registry.get("edges", []):
        graph[edge["from"]].append(edge["to"])
        all_nodes.add(edge["from"])
        all_nodes.add(edge["to"])
    
    # Detect cycles using DFS
    visited = set()
    rec_stack = set()  # recursion stack
    cycles_found = []
    
    def dfs(node, path):
        visited.add(node)
        rec_stack.add(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor, path + [neighbor]):
                    return True
            elif neighbor in rec_stack:
                # Found a cycle
                cycle_start_idx = path.index(neighbor) if neighbor in path else 0
                cycle = path[cycle_start_idx:] + [neighbor]
                cycles_found.append(cycle)
                return True
        
        rec_stack.remove(node)
        return False
    
    # Run DFS from each unvisited node
    for node in all_nodes:
        if node not in visited:
            dfs(node, [node])
    
    return cycles_found

if __name__ == "__main__":
    import json
    from src.dag.dag_builder import build_dag
    
    try:
        with open("registry/registry_v0.json", "r") as f:
            registry = json.load(f)
        
        cycles = detect_cycles(registry)
        print("Cycles detected:", json.dumps(cycles, indent=2))
    except Exception as e:
        print(f"Error: {e}")
