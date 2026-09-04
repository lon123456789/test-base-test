from typing import Dict, Any


class OpportunityScoring:
    def __init__(self):
        pass

    def score(self, market: Dict[str, Any], security: Dict[str, Any]) -> Dict[str, Any]:
        """
        market: output from CoinGeckoProvider
        security: output from SecurityFilter
        """

        if security["hard_reject_reason"]:
            return {
                "score": 0,
                "reason": f"hard_reject:{security['hard_reject_reason']}",
                "opportunity": "none"
            }

        score = 0
        reasons = []

        # Price momentum
        score += self._momentum_score(market, reasons)

        # Liquidity strength
        score += self._liquidity_score(security, reasons)

        # Holder distribution
        score += self._holder_score(security, reasons)

        # Soft penalties
        score -= len(security["soft_penalties"]) * 5

        # Normalize
        final_score = max(0, min(score, 100))

        return {
            "score": final_score,
            "reasons": reasons,
            "soft_penalties": security["soft_penalties"],
            "opportunity": self._label(final_score)
        }

    def _momentum_score(self, market: Dict[str, Any], reasons: list) -> int:
        score = 0

        p1h = market.get("price_change_percentage_1h", 0)
        p24h = market.get("price_change_percentage_24h", 0)
        p7d = market.get("price_change_percentage_7d", 0)

        if p1h > 0:
            score += 5
            reasons.append("positive_1h")
        if p24h > 0:
            score += 10
            reasons.append("positive_24h")
        if p7d > 0:
            score += 15
            reasons.append("positive_7d")

        return score

    def _liquidity_score(self, security: Dict[str, Any], reasons: list) -> int:
        liq = security.get("liquidity_usd", 0)
        if liq > 20000:
            reasons.append("strong_liquidity")
            return 20
        if liq > 5000:
            reasons.append("medium_liquidity")
            return 10
        return 0

    def _holder_score(self, security: Dict[str, Any], reasons: list) -> int:
        top10 = security.get("holder_top10_pct", 0)
        if top10 < 20:
            reasons.append("healthy_distribution")
            return 15
        if top10 < 40:
            reasons.append("acceptable_distribution")
            return 5
        return 0

    def _label(self, score: int) -> str:
        if score >= 80:
            return "high_opportunity"
        if score >= 50:
            return "medium_opportunity"
        if score >= 20:
            return "low_opportunity"
        return "none"


if __name__ == "__main__":
    print("OpportunityScoring ready.")
