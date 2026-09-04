import requests
from typing import Optional, Dict, Any


class BaseScanProvider:
    BASE_URL = "https://api.basescan.org/api"

    def __init__(self, api_key: str, session: Optional[requests.Session] = None):
        self.api_key = api_key
        self.session = session or requests.Session()

    def _get(self, params: Dict[str, Any]) -> Any:
        params["apikey"] = self.api_key
        resp = self.session.get(self.BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "1":
            raise ValueError(f"BaseScan error: {data}")
        return data.get("result")

    def get_contract_source(self, contract_address: str) -> Dict[str, Any]:
        result = self._get({
            "module": "contract",
            "action": "getsourcecode",
            "address": contract_address
        })

        item = result[0]
        return {
            "contract_name": item.get("ContractName"),
            "compiler_version": item.get("CompilerVersion"),
            "verified": item.get("SourceCode") not in ["", None],
            "source_code": item.get("SourceCode"),
            "proxy": item.get("Proxy") == "1",
            "implementation": item.get("Implementation"),
            "contract_address": contract_address
        }

    def get_contract_creation(self, contract_address: str) -> Dict[str, Any]:
        result = self._get({
            "module": "contract",
            "action": "getcontractcreation",
            "contractaddresses": contract_address
        })

        item = result[0]
        return {
            "contract_address": contract_address,
            "creator": item.get("creator"),
            "tx_hash": item.get("txHash"),
            "timestamp": item.get("timestamp")
        }

    def get_token_holders(self, contract_address: str) -> Dict[str, Any]:
        result = self._get({
            "module": "token",
            "action": "getTokenHolderList",
            "contractaddress": contract_address,
            "page": 1,
            "offset": 100
        })

        holders = []
        for h in result:
            holders.append({
                "address": h.get("HolderAddress"),
                "balance": int(h.get("TokenHolderQuantity", "0"))
            })

        return {
            "contract_address": contract_address,
            "holders": holders
        }

    def get_authorities(self, contract_address: str) -> Dict[str, Any]:
        """
        Detect mint / blacklist / upgrade authority by scanning ABI.
        """
        result = self._get({
            "module": "contract",
            "action": "getabi",
            "address": contract_address
        })

        abi = result
        mint = any("mint" in str(x).lower() for x in abi)
        blacklist = any("blacklist" in str(x).lower() for x in abi)
        upgrade = any("upgrade" in str(x).lower() for x in abi)

        return {
            "contract_address": contract_address,
            "mint_authority": mint,
            "blacklist_authority": blacklist,
            "upgrade_authority": upgrade
        }


if __name__ == "__main__":
    provider = BaseScanProvider(api_key="YOUR_API_KEY")
    example = "0x0000000000000000000000000000000000000000"
    print(provider.get_contract_source(example))
