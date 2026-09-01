import json
from collections import defaultdict

def build_dag(registry_path):
    with open(registry_path, "r") as f:
        registry = json.load(f)

    dag = defaultdict(list)

    for feature in registry["features"]:
        for parent in feature.get("depends_on", []):
            dag[parent].append(feature["feature_id"])

    for edge in registry["edges"]:
        dag[edge["from"]].append(edge["to"])

    return dag

if __name__ == "__main__":
    dag = build_dag("registry/registry_v0.json")
    print(json.dumps(dag, indent=2))