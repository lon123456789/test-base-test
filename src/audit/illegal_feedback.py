def audit_illegal_feedback(dag):
    violations = []
    forbidden = ["Clustering", "Fusion_Direction", "Fusion_Strength", "Fusion_Quality"]

    for node, children in dag.items():
        for child in children:
            if node in forbidden and child in forbidden:
                violations.append((node, child))

    return violations