import unittest
from unittest.mock import MagicMock

from pipeline.pipeline import Pipeline


class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = Pipeline(basescan_api_key="DUMMY")

        # Mock providers
        self.pipeline.cg.get_token_market_data = MagicMock(return_value={
            "current_price": 1.23,
            "market_cap": 1000000,
            "fdv": 1500000,
            "total_volume": 50000,
            "price_change_percentage_1h": 2.0,
            "price_change_percentage_24h": 5.0,
            "price_change_percentage_7d": 10.0
        })

        self.pipeline.gt.get_pool_data = MagicMock(return_value={
            "liquidity_usd": 25000,
            "volume_24h": 10000
        })

        self.pipeline.bs.get_contract_source = MagicMock(return_value={
            "verified": True,
            "proxy": False,
            "implementation": None
        })

        self.pipeline.bs.get_contract_creation = MagicMock(return_value={
            "creator": "0xDEADBEEF",
            "timestamp": 2000
        })

        self.pipeline.bs.get_token_holders = MagicMock(return_value={
            "holders": [
                {"address": "0xAAA", "balance": 5000},
                {"address": "0xBBB", "balance": 3000},
                {"address": "0xCCC", "balance": 2000}
            ]
        })

        self.pipeline.bs.get_authorities = MagicMock(return_value={
            "mint_authority": False,
            "blacklist_authority": False,
            "upgrade_authority": False
        })

    def test_pipeline_output(self):
        result = self.pipeline.run(
            token_id="bitcoin",
            token_address="0x123",
            pool_address="0xPOOL"
        )

        self.assertIn("market", result)
        self.assertIn("security", result)
        self.assertIn("opportunity", result)

        self.assertGreater(result["opportunity"]["score"], 0)
        self.assertEqual(result["security"]["hard_reject_reason"], None)


if __name__ == "__main__":
    unittest.main()
