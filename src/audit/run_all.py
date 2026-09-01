import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

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
    # Load registry
    try:
        with open("registry/registry_v0.json", "r") as f:
            registry = json.load(f)
    except FileNotFoundError:
        print("Error: registry/registry_v0.json not found")
        return {}
    except json.JSONDecodeError:
        print("Error: registry/registry_v0.json is not valid JSON")
        return {}
    
    # Debug: Print FUS_DIRECTION and FUS_STRENGTH features
    fus_features = {f["feature_id"]: f for f in registry["features"] 
                   if f["feature_id"] in ["FUS_DIRECTION", "FUS_STRENGTH"]}
    
    # Run all audit checks
    missing_conf_result = audit_missing_confidence(registry)
    
    report = {
        "cycles": detect_cycles(registry),
        "future_leakage": audit_future_leakage(registry),
        "ownership": audit_ownership(registry),
        "illegal_feedback": audit_illegal_feedback(registry),
        "cluster_scope": audit_cluster_scope(registry),
        "double_count": audit_double_count(registry),
        "missing_confidence": missing_conf_result
    }
    
    return report

if __name__ == "__main__":
    report = run_all()
    print(json.dumps(report, indent=2))
