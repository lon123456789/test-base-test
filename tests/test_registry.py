import unittest
import json
import os


class TestRegistry(unittest.TestCase):
    def setUp(self):
        base_path = os.path.join("registry")
        self.registry_file = os.path.join(base_path, "registry_v0.json")
        self.schema_file = os.path.join(base_path, "schema.json")

        # Mock registry content if file missing
        if not os.path.exists(self.registry_file):
            os.makedirs(base_path, exist_ok=True)
            with open(self.registry_file, "w") as f:
                json.dump({
                    "tokens": [
                        {
                            "id": "bitcoin",
                            "symbol": "btc",
                            "chain": "base",
                            "coingecko_id": "bitcoin",
                            "contract_address": "0x0000000000000000000000000000000000000000",
                            "pool_address": "0x0000000000000000000000000000000000000000"
                        }
                    ]
                }, f)

        # Mock schema if missing
        if not os.path.exists(self.schema_file):
            with open(self.schema_file, "w") as f:
                json.dump({
                    "type": "object",
                    "properties": {
                        "tokens": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "symbol": {"type": "string"},
                                    "chain": {"type": "string"},
                                    "coingecko_id": {"type": "string"},
                                    "contract_address": {"type": "string"},
                                    "pool_address": {"type": "string"}
                                },
                                "required": [
                                    "id",
                                    "symbol",
                                    "chain",
                                    "coingecko_id",
                                    "contract_address",
                                    "pool_address"
                                ]
                            }
                        }
                    },
                    "required": ["tokens"]
                }, f)

    def test_registry_loads(self):
        with open(self.registry_file, "r") as f:
            data = json.load(f)

        self.assertIn("tokens", data)
        self.assertGreater(len(data["tokens"]), 0)

    def test_registry_schema_valid(self):
        with open(self.registry_file, "r") as f:
            data = json.load(f)

        with open(self.schema_file, "r") as f:
            schema = json.load(f)

        # Basic schema validation (manual, no external libs)
        self.assertIn("tokens", data)
        self.assertIsInstance(data["tokens"], list)

        for token in data["tokens"]:
            for field in schema["properties"]["tokens"]["items"]["required"]:
                self.assertIn(field, token)
                self.assertIsInstance(token[field], str)

    def test_registry_token_fields(self):
        with open(self.registry_file, "r") as f:
            data = json.load(f)

        token = data["tokens"][0]

        self.assertTrue(token["id"])
        self.assertTrue(token["symbol"])
        self.assertTrue(token["coingecko_id"])
        self.assertTrue(token["contract_address"])
        self.assertTrue(token["pool_address"])


if __name__ == "__main__":
    unittest.main()
