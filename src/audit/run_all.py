import json
import sys
import os
from pathlib import Path

# Force reload of all modules
for mod in list(sys.modules.keys()):
    if mod.startswith('src.'):
        del sys.modules[mod]

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
    except json.JSONDecodeError as e:
        print(f"Error: registry/registry_v0.json is not valid JSON: {e}")
        return {}
    
    # Debug: Check registry content
    print(f"=== REGISTRY LOADED ===", file=sys.stderr)
    print(f"Total features: {len(registry.get('features', []))}", file=sys.stderr)
    
    # Find and print FUS_DIRECTION and FUS_STRENGTH
    for feat in registry.get("features", []):
        if feat["feature_id"] in ["FUS_DIRECTION", "FUS_STRENGTH"]:
            print(f"{feat['feature_id']}: role={feat.get('primary_role')}, rule={feat.get('missing_data_rule')}", file=sys.stderr)
    
    print(f"=== CALLING AUDIT FUNCTIONS ===", file=sys.stderr)
    sys.stderr.flush()
    
    # Run all audit checks
    missing_conf_result = audit_missing_confidence(registry)
    
    print(f"=== MISSING_CONFIDENCE RETURNED: {len(missing_conf_result)} violations ===", file=sys.stderr)
    sys.stderr.flush()
    
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
