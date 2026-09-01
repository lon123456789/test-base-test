def detect_cycles(dag):
    visited = set()
    stack = set()
    cycles = []

    def dfs(node):
        if node in stack:
            cycles.append(node)
            return
        if node in visited:
            return

        visited.add(node)
        stack.add(node)

        for child in dag.get(node, []):
            dfs(child)

        stack.remove(node)

    for node in dag:
        dfs(node)

    return cycles

if __name__ == "__main__":
    import json
    from dag_builder import build_dag

    dag = build_dag("registry/registry_v0.json")
    cycles = detect_cycles(dag)
    print("CYCLES:", cycles)