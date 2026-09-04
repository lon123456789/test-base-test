import requests
from typing import Optional, Dict, Any


class GeckoTerminalProvider:
    BASE_URL = "https://api.geckoterminal.com/api/v2"

    def __init__(self, session: Optional[requests.Session] = None):
        self.session = session or requests.Session()

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.BASE_URL}{path}"
        resp = self.session.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_pool_data(self, pool_address: str) -> Dict[str, Any]:
        """
        pool_address: address of the LP pool on Base (or any chain supported)
        """
        data = self._get(f"/pools/{pool_address}")

        pool = data.get("data", {})
        attr = pool.get("attributes", {})

        return {
            "address": pool_address,
            "name": attr.get("name"),
            "reserve_usd": attr.get("reserve_in_usd"),
            "volume_24h": attr.get("volume_usd", {}).get("h24"),
            "price_token0": attr.get("token0_price"),
            "price_token1": attr.get("token1_price"),
            "fdv": attr.get("fdv"),
            "liquidity_usd": attr.get("reserve_in_usd"),
            "updated_at": attr.get("updated_at"),
        }

    def get_token_price(self, token_address: str) -> Dict[str, Any]:
        """
        token_address: contract address of the token
        """
        data = self._get(f"/tokens/{token_address}")

        token = data.get("data", {})
        attr = token.get("attributes", {})

        return {
            "address": token_address,
            "symbol": attr.get("symbol"),
            "name": attr.get("name"),
            "price_usd": attr.get("price_usd"),
            "fdv": attr.get("fdv"),
            "volume_24h": attr.get("volume_usd", {}).get("h24"),
            "liquidity_usd": attr.get("liquidity_usd"),
            "updated_at": attr.get("updated_at"),
        }


if __name__ == "__main__":
    provider = GeckoTerminalProvider()
    # Example pool on Base — replace with real pool
    example_pool = "0x0000000000000000000000000000000000000000"
    print(provider.get_pool_data(example_pool))
