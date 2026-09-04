import requests
from typing import Optional, Dict, Any


class CoinGeckoProvider:
    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self, session: Optional[requests.Session] = None):
        self.session = session or requests.Session()

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.BASE_URL}{path}"
        resp = self.session.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_token_market_data(self, token_id: str, vs_currency: str = "usd") -> Dict[str, Any]:
        """
        token_id: CoinGecko ID (e.g. 'bitcoin', 'ethereum', 'base')
        vs_currency: fiat or crypto (default 'usd')
        """
        data = self._get(
            "/coins/markets",
            params={
                "vs_currency": vs_currency,
                "ids": token_id,
                "order": "market_cap_desc",
                "per_page": 1,
                "page": 1,
                "sparkline": "false",
                "price_change_percentage": "1h,24h,7d"
            },
        )
        if not data:
            raise ValueError(f"No market data returned for token_id={token_id}")

        item = data[0]
        return {
            "id": item.get("id"),
            "symbol": item.get("symbol"),
            "name": item.get("name"),
            "current_price": item.get("current_price"),
            "market_cap": item.get("market_cap"),
            "fdv": item.get("fully_diluted_valuation"),
            "total_volume": item.get("total_volume"),
            "price_change_percentage_1h": item.get("price_change_percentage_1h_in_currency"),
            "price_change_percentage_24h": item.get("price_change_percentage_24h_in_currency"),
            "price_change_percentage_7d": item.get("price_change_percentage_7d_in_currency"),
            "circulating_supply": item.get("circulating_supply"),
            "total_supply": item.get("total_supply"),
            "max_supply": item.get("max_supply"),
            "last_updated": item.get("last_updated"),
        }

    def get_token_detail(self, token_id: str) -> Dict[str, Any]:
        """
        More detailed info (categories, links, description, etc.)
        """
        data = self._get(
            f"/coins/{token_id}",
            params={
                "localization": "false",
                "tickers": "false",
                "market_data": "false",
                "community_data": "false",
                "developer_data": "false",
                "sparkline": "false",
            },
        )
        return {
            "id": data.get("id"),
            "symbol": data.get("symbol"),
            "name": data.get("name"),
            "categories": data.get("categories") or [],
            "links": data.get("links") or {},
            "contract_address": self._extract_contract_address(data),
        }

    @staticmethod
    def _extract_contract_address(data: Dict[str, Any]) -> Optional[str]:
        platforms = data.get("platforms") or {}
        # Example: for Base or Ethereum, you can adjust this logic later
        for _, addr in platforms.items():
            if addr:
                return addr
        return None


if __name__ == "__main__":
    provider = CoinGeckoProvider()
    # Example usage: change 'bitcoin' to your target token_id
    md = provider.get_token_market_data("bitcoin")
    print("Market data:", md)
