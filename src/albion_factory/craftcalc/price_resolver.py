from __future__ import annotations

from dataclasses import dataclass, field

from albion_factory.craftcalc.models import CraftPricePoint


@dataclass
class PriceResolutionResult:
    item_id: str
    city: str
    selected_price: float | None
    selected_side: str | None
    used_fallback: bool = False
    missing_reasons: list[str] = field(default_factory=list)


class PriceResolver:
    """Resolves city-specific prices for craft calculator foundations.

    Phase 3 skeleton responsibilities:
    - select buy/sell side
    - prefer freshest matching city record
    - support simple fallback when exact side is missing
    """

    def __init__(self, prices: list[CraftPricePoint]) -> None:
        self._prices = prices

    def find_prices(self, item_id: str, city: str) -> list[CraftPricePoint]:
        return [p for p in self._prices if p.item_id == item_id and p.city == city]

    def resolve(
        self,
        item_id: str,
        city: str,
        *,
        prefer_buy_order: bool = False,
    ) -> PriceResolutionResult:
        matches = self.find_prices(item_id=item_id, city=city)
        if not matches:
            return PriceResolutionResult(
                item_id=item_id,
                city=city,
                selected_price=None,
                selected_side=None,
                used_fallback=False,
                missing_reasons=[f"No price points found for {item_id} in {city}"],
            )

        primary_side = "buy" if prefer_buy_order else "sell"
        fallback_side = "sell" if prefer_buy_order else "buy"

        selected = self._select_side(matches, primary_side)
        if selected is not None:
            return PriceResolutionResult(
                item_id=item_id,
                city=city,
                selected_price=selected,
                selected_side=primary_side,
                used_fallback=False,
            )

        fallback = self._select_side(matches, fallback_side)
        if fallback is not None:
            return PriceResolutionResult(
                item_id=item_id,
                city=city,
                selected_price=fallback,
                selected_side=fallback_side,
                used_fallback=True,
                missing_reasons=[f"Primary side '{primary_side}' missing, fallback side used"],
            )

        return PriceResolutionResult(
            item_id=item_id,
            city=city,
            selected_price=None,
            selected_side=None,
            used_fallback=False,
            missing_reasons=[f"Both buy and sell price sides missing for {item_id} in {city}"],
        )

    def _select_side(self, matches: list[CraftPricePoint], side: str) -> float | None:
        for price_point in matches:
            if side == "buy" and price_point.buy_price_max is not None:
                return price_point.buy_price_max
            if side == "sell" and price_point.sell_price_min is not None:
                return price_point.sell_price_min
        return None