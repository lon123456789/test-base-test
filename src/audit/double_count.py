def audit_double_count(registry):
    concept_paths = {}
    violations = []

    for f in registry["features"]:
        concept = f["semantic_concept"]
        if concept not in concept_paths:
            concept_paths[concept] = 1
        else:
            concept_paths[concept] += 1

    for concept, count in concept_paths.items():
        if count > 1:
            violations.append((concept, count))

    return violations