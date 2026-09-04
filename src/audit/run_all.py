import json
import sys
from pathlib import Path

# Ensure project root is in PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.dag.dag_validator import detect_cycles
from src.audit.future_leakage import audit_future_leakage
from src.audit.ownership import audit_ownership
from src.audit.illegal_feedback import audit_illegal_feedback
from src.audit.cluster_scope import audit_cluster_scope
from src.audit.double_count import audit_double_count
from src.audit.missing_confidence import audit_missing_confidence


def run_all():
    """
    Execute all audit checks and return consolidated report.
    """
    registry_path = PROJECT_ROOT / "registry" / "registry_v0.json"

    try:
        with open(registry_path, "r") as f:
            registry = json.load(f)
    except FileNotFoundError:
        print(f"Error: {registry_path} not found")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: registry_v0.json invalid JSON: {e}")
        return {}

    report = {
        "cycles": detect_cycles(registry),
        "future_leakage": audit_future_leakage(registry),
        "ownership": audit_ownership(registry),
        "illegal_feedback": audit_illegal_feedback(registry),
        "cluster_scope": audit_cluster_scope(registry),
        "double_count": audit_double_count(registry),
        "missing_confidence": audit_missing_confidence(registry)
    }

    return report


if __name__ == "__main__":
    print(json.dumps(run_all(), indent=2))
