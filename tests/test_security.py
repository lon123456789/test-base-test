import unittest
from security.security_filter import SecurityFilter


class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.sf = SecurityFilter()

        self.contract = {
            "verified": True,
            "proxy": False,
            "implementation": None
        }

        self.creation = {
            "creator": "0xDEADBEEF",
            "timestamp": 2000
        }

        self.holders = {
            "holders": [
                {"address": "0xDEADBEEF", "balance": 5000},
                {"address": "0xAAA", "balance": 3000},
                {"address": "0xBBB", "balance": 2000}
            ]
        }

        self.authorities = {
            "mint_authority": False,
            "blacklist_authority": False,
            "upgrade_authority": False
        }

        self.pool = {
            "liquidity_usd": 25000
        }

    def test_security_profile_valid(self):
        profile = self.sf.build_profile(
            contract=self.contract,
            creation=self.creation,
            holders=self.holders,
            authorities=self.authorities,
            pool=self.pool,
            honeypot_status="safe"
        )

        self.assertEqual(profile["hard_reject_reason"], None)
        self.assertGreater(profile["liquidity_usd"], 5000)
        self.assertLess(profile["holder_top10_pct"], 100)

    def test_hard_reject_low_liquidity(self):
        pool = {"liquidity_usd": 1000}

        profile = self.sf.build_profile(
            contract=self.contract,
            creation=self.creation,
            holders=self.holders,
            authorities=self.authorities,
            pool=pool,
            honeypot_status="safe"
        )

        self.assertEqual(profile["hard_reject_reason"], "low_liquidity")

    def test_hard_reject_honeypot(self):
        profile = self.sf.build_profile(
            contract=self.contract,
            creation=self.creation,
            holders=self.holders,
            authorities=self.authorities,
            pool=self.pool,
            honeypot_status="honeypot"
        )

        self.assertEqual(profile["hard_reject_reason"], "honeypot")


if __name__ == "__main__":
    unittest.main()
