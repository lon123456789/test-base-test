import argparse
import json
from pipeline.pipeline import Pipeline


def main():
    parser = argparse.ArgumentParser(description="Token Analysis CLI")
    parser.add_argument("--token-id", required=True, help="CoinGecko token id")
    parser.add_argument("--contract", required=True, help="Contract address")
    parser.add_argument("--pool", required=True, help="Pool address")
    parser.add_argument("--basescan-key", required=True, help="BaseScan API key")

    args = parser.parse_args()

    pipeline = Pipeline(basescan_api_key=args.basescan_key)

    result = pipeline.run(
        token_id=args.token_id,
        token_address=args.contract,
        pool_address=args.pool
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
