import unittest
from src.opportunity.opportunity_scoring import OpportunityScoring


class TestOpportunity(unittest.TestCase):
    def setUp(self):
        self.scoring = OpportunityScoring()

        self.market = {
            "price_change_percentage_1h": 2.0,
            "price_change_percentage_24h": 5.0,
            "price_change_percentage_7d": 10.0
        }

        self.security = {
            "liquidity_usd": 25000,
            "holder_top1_pct": 10,
            "holder_top10_pct": 25,
            "deployer_hold_pct": 5,
            "soft_penalties": [],
            "hard_reject_reason": None
        }

    def test_opportunity_score_positive(self):
        result = self.scoring.score(self.market, self.security)

        self.assertGreater(result["score"], 0)
        self.assertIn("positive_1h", result["reasons"])
        self.assertIn("strong_liquidity", result["reasons"])
        self.assertIn("healthy_distribution", result["reasons"])
        self.assertEqual(result["opportunity"], "high_opportunity")

    def test_hard_reject(self):
        sec = dict(self.security)
        sec["hard_reject_reason"] = "honeypot"

        result = self.scoring.score(self.market, sec)

        self.assertEqual(result["score"], 0)
        self.assertEqual(result["opportunity"], "none")
        self.assertIn("hard_reject:honeypot", result["reason"])


if __name__ == "__main__":
    unittest.main()
