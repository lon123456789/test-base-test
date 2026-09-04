from src.providers.coingecko_provider import CoinGeckoProvider
from src.providers.geckoterminal_provider import GeckoTerminalProvider
from src.providers.basescan_provider import BaseScanProvider

from src.security.security_filter import SecurityFilter
from src.opportunity.opportunity_scoring import OpportunityScoring


class Pipeline:
    def __init__(self, basescan_api_key: str):
        self.cg = CoinGeckoProvider()
        self.gt = GeckoTerminalProvider()
        self.bs = BaseScanProvider(api_key=basescan_api_key)

        self.security = SecurityFilter()
        self.opportunity = OpportunityScoring()

    def run(self, token_id: str, token_address: str, pool_address: str) -> dict:
        # Market data
        market = self.cg.get_token_market_data(token_id)

        # GeckoTerminal pool data
        pool = self.gt.get_pool_data(pool_address)

        # BaseScan data
        contract = self.bs.get_contract_source(token_address)
        creation = self.bs.get_contract_creation(token_address)
        holders = self.bs.get_token_holders(token_address)
        authorities = self.bs.get_authorities(token_address)

        # Honeypot status (placeholder)
        honeypot_status = "safe"

        # Security profile
        security_profile = self.security.build_profile(
            contract=contract,
            creation=creation,
            holders=holders,
            authorities=authorities,
            pool=pool,
            honeypot_status=honeypot_status
        )

        # Opportunity score
        opportunity_score = self.opportunity.score(
            market=market,
            security=security_profile
        )

        return {
            "market": market,
            "security": security_profile,
            "opportunity": opportunity_score
        }


if __name__ == "__main__":
    pipeline = Pipeline(basescan_api_key="YOUR_API_KEY")

    result = pipeline.run(
        token_id="bitcoin",
        token_address="0x0000000000000000000000000000000000000000",
        pool_address="0x0000000000000000000000000000000000000000"
    )

    print(result)
