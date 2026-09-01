def audit_ownership(registry):
    concept_map = {}
    violations = []

    for f in registry["features"]:
        concept = f["semantic_concept"]
        owner = f["owner_engine"]

        if concept not in concept_map:
            concept_map[concept] = owner
        else:
            if concept_map[concept] != owner:
                violations.append((concept, concept_map[concept], owner))

    return violations