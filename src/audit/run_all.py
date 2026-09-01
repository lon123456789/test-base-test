import json
from src.dag.dag_builder import build_dag
from src.dag.dag_validator import detect_cycles
from src.audit.future_leakage import audit_future_leakage
from src.audit.ownership import audit_ownership
from src.audit.illegal_feedback import audit_illegal_feedback
from src.audit.cluster_scope import audit_cluster_scope
from src.audit.double_count import audit_double_count
from src.audit.missing_confidence import audit_missing_confidence

def run_all():
    with open("registry/registry_v0.json") as f:
        registry = json.load(f)

    dag = build_dag("registry/registry_v0.json")

    report = {
        "cycles": detect_cycles(dag),
        "future_leakage": audit_future_leakage(registry),
        "ownership": audit_ownership(registry),
        "illegal_feedback": audit_illegal_feedback(dag),
        "cluster_scope": audit_cluster_scope(registry),
        "double_count": audit_double_count(registry),
        "missing_confidence": audit_missing_confidence(registry)
    }

    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    run_all()