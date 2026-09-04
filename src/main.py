from pipeline.pipeline import Pipeline
import json
import os


def load_registry():
    path = os.path.join("registry", "registry_v0.json")
    with open(path, "r") as f:
        return json.load(f)


def run_all():
    registry = load_registry()
    pipeline = Pipeline(basescan_api_key="YOUR_API_KEY")

    results = []

    for token in registry["tokens"]:
        result = pipeline.run(
            token_id=token["coingecko_id"],
            token_address=token["contract_address"],
            pool_address=token["pool_address"]
        )
        results.append({
            "id": token["id"],
            "symbol": token["symbol"],
            "result": result
        })

    return results


if __name__ == "__main__":
    output = run_all()
    print(json.dumps(output, indent=2))
