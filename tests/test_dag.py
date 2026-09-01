from src.dag.dag_builder import build_dag

def test_dag_build():
    dag = build_dag("registry/registry_v0.json")
    assert isinstance(dag, dict)