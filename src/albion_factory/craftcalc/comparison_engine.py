from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class BuyVsCraftComparison:
    item_id: str
    city: str
    craft_cost: float
    buy_cost: float
    preferred_action: str
    savings: float


@dataclass
class CityComparisonResult:
    item_id: str
    compared_cities: list[str] = field(default_factory=list)
    cheapest_city: str | None = None
    cheapest_price: float | None = None


@dataclass
class RefineCraftSellComparison:
    chain_id: str
    total_input_cost: float
    total_output_value: float
    net_profit: float


@dataclass
class CheapestInputPathResult:
    item_id: str
    chosen_inputs: dict[str, float] = field(default_factory=dict)
    total_cost: float = 0.0


class ComparisonEngine:
    """Initial comparison engine for craft calculator.

    Phase 5 scope:
    - craft vs buy
    - city compare
    - future refine->craft->sell compare hook
    """

    def compare_buy_vs_craft(
        self,
        *,
        item_id: str,
        city: str,
        craft_cost: float,
        buy_cost: float,
    ) -> BuyVsCraftComparison:
        preferred_action = "craft" if craft_cost <= buy_cost else "buy"
        savings = abs(buy_cost - craft_cost)
        return BuyVsCraftComparison(
            item_id=item_id,
            city=city,
            craft_cost=craft_cost,
            buy_cost=buy_cost,
            preferred_action=preferred_action,
            savings=round(savings, 2),
        )

    def compare_cities(self, *, item_id: str, city_prices: dict[str, float]) -> CityComparisonResult:
        if not city_prices:
            return CityComparisonResult(item_id=item_id)

        cheapest_city = min(city_prices, key=city_prices.get)
        return CityComparisonResult(
            item_id=item_id,
            compared_cities=sorted(city_prices.keys()),
            cheapest_city=cheapest_city,
            cheapest_price=city_prices[cheapest_city],
        )

    def compare_refine_craft_sell_chain(
        self,
        *,
        chain_id: str,
        step_costs: list[float],
        sell_value: float,
    ) -> RefineCraftSellComparison:
        total_input_cost = round(sum(step_costs), 2)
        net_profit = round(sell_value - total_input_cost, 2)
        return RefineCraftSellComparison(
            chain_id=chain_id,
            total_input_cost=total_input_cost,
            total_output_value=round(sell_value, 2),
            net_profit=net_profit,
        )

    def cheapest_input_chain(self, *, item_id: str, candidate_inputs: dict[str, float]) -> CheapestInputPathResult:
        ordered = dict(sorted(candidate_inputs.items(), key=lambda item: item[1]))
        total_cost = round(sum(ordered.values()), 2)
        return CheapestInputPathResult(
            item_id=item_id,
            chosen_inputs=ordered,
            total_cost=total_cost,
        )