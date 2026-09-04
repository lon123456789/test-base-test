from typing import Dict, Any


class SecurityFilter:
    HARD_RULES = {
        "liquidity_min": 5000,
        "deployer_max_pct": 50,
        "contract_age_min_minutes": 1440  # 24 hours
    }

    def __init__(self):
        pass

    def build_profile(
        self,
        contract: Dict[str, Any],
        creation: Dict[str, Any],
        holders: Dict[str, Any],
        authorities: Dict[str, Any],
        pool: Dict[str, Any],
        honeypot_status: str
    ) -> Dict[str, Any]:

        holder_balances = [h["balance"] for h in holders["holders"]]
        total_supply = sum(holder_balances) if holder_balances else 0

        top1_pct = (holder_balances[0] / total_supply * 100) if total_supply else 0
        top10_pct = (sum(holder_balances[:10]) / total_supply * 100) if total_supply else 0

        deployer_hold_pct = self._calc_deployer_pct(creation["creator"], holders["holders"], total_supply)

        profile = {
            "contract_verified": contract["verified"],
            "contract_age_minutes": int(creation["timestamp"]),
            "proxy_pattern": self._proxy_pattern(contract),
            "mint_authority": authorities["mint_authority"],
            "blacklist_authority": authorities["blacklist_authority"],
            "upgrade_authority": authorities["upgrade_authority"],
            "honeypot_status": honeypot_status,
            "liquidity_usd": pool.get("liquidity_usd", 0),
            "holder_top1_pct": top1_pct,
            "holder_top10_pct": top10_pct,
            "deployer_hold_pct": deployer_hold_pct,
            "deployer_cluster_risk": "unknown",
            "soft_penalties": [],
            "hard_reject_reason": None
        }

        self._apply_hard_rules(profile)
        self._apply_soft_rules(profile)

        return profile

    def _proxy_pattern(self, contract: Dict[str, Any]) -> str:
        if not contract["proxy"]:
            return "none"
        if contract["implementation"]:
            return "safe"
        return "unsafe"

    def _calc_deployer_pct(self, deployer: str, holders: Any, total_supply: int) -> float:
        for h in holders:
            if h["address"].lower() == deployer.lower():
                return (h["balance"] / total_supply * 100) if total_supply else 0
        return 0.0

    def _apply_hard_rules(self, profile: Dict[str, Any]):
        if profile["honeypot_status"] == "honeypot":
            profile["hard_reject_reason"] = "honeypot"
        elif profile["liquidity_usd"] < self.HARD_RULES["liquidity_min"]:
            profile["hard_reject_reason"] = "low_liquidity"
        elif profile["deployer_hold_pct"] > self.HARD_RULES["deployer_max_pct"]:
            profile["hard_reject_reason"] = "deployer_owns_too_much"
        elif profile["contract_age_minutes"] < self.HARD_RULES["contract_age_min_minutes"]:
            profile["hard_reject_reason"] = "contract_too_new"
        elif profile["mint_authority"]:
            profile["hard_reject_reason"] = "mint_authority"
        elif profile["blacklist_authority"]:
            profile["hard_reject_reason"] = "blacklist_authority"
        elif profile["upgrade_authority"]:
            profile["hard_reject_reason"] = "upgrade_authority"

    def _apply_soft_rules(self, profile: Dict[str, Any]):
        if 5000 <= profile["liquidity_usd"] < 20000:
            profile["soft_penalties"].append("low_liquidity_soft")

        if 20 <= profile["holder_top1_pct"] <= 50:
            profile["soft_penalties"].append("high_top1_soft")

        if 20 <= profile["holder_top10_pct"] <= 50:
            profile["soft_penalties"].append("high_top10_soft")

        if 10 <= profile["deployer_hold_pct"] <= 50:
            profile["soft_penalties"].append("deployer_soft")

        if profile["proxy_pattern"] == "safe":
            profile["soft_penalties"].append("upgradeable_soft")


if __name__ == "__main__":
    print("SecurityFilter ready.")
