# Feature Registry Audit System

## Project Structure

```
project-root/
│
├── registry/
│   ├── registry_v0.json
│   └── schema.json
│
├── src/
│   ├── dag/
│   │   ├── dag_builder.py
│   │   └── dag_validator.py
│   │
│   └── audit/
│       ├── future_leakage.py
│       ├── ownership.py
│       ├── illegal_feedback.py
│       ├── cluster_scope.py
│       ├── double_count.py
│       ├── missing_confidence.py
│       └── run_all.py
│
├── output/
│   └── validated_registry_v1.json
│
└── tests/
    ├── test_registry.py
    ├── test_dag.py
    └── test_audit.py
```

## Overview

This system provides:

- **DAG Builder**: Constructs directed acyclic graphs from feature dependencies
- **DAG Validator**: Detects cycles in feature dependencies
- **Audit Modules**: Seven independent audit functions for data quality and integrity

## Audit Checks

1. **future_leakage.py** - Detects when features without future data depend on features with future data
2. **ownership.py** - Ensures each semantic concept has a single owner engine
3. **illegal_feedback.py** - Prevents feedback loops between forbidden nodes
4. **cluster_scope.py** - Validates cluster adjustment scopes
5. **double_count.py** - Identifies duplicate semantic concepts
6. **missing_confidence.py** - Checks missing data handling rules
7. **run_all.py** - Orchestrates all audit checks

## Version

**v0.0** - Skeleton foundation
**v0.1** (coming soon) - Complete audit with 8 engine registry
