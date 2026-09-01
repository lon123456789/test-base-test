import json
import jsonschema

def test_registry_schema():
    with open("registry/schema.json") as s:
        schema = json.load(s)
    with open("registry/registry_v0.json") as r:
        registry = json.load(r)

    jsonschema.validate(registry, schema)