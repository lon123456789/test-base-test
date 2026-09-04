from typing import Dict, Any


class SecurityFilter:
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

        top10_pct = (sum(holder_balances[:10]) / total_supply * 100) if total_supply else 0
        if top10_pct >= 100:
            top10_pct = 99.0

        liquidity = pool.get("liquidity_usd", 0)

        # HARD RULES
        if honeypot_status == "honeypot":
            hard = "honeypot"
        elif liquidity < 5000:
            hard = "low_liquidity"
        else:
            hard = None

        return {
            "hard_reject_reason": hard,
            "liquidity_usd": liquidity,
            "holder_top10_pct": top10_pct,
            "soft_penalties": []
        }
