from albion_factory.craftcalc import CraftCalculationRequest, CraftRuleSet
from albion_factory.craftcalc.profit_engine import ProfitCalculationInput, ProfitEngine


def test_profit_engine_basic_profitability() -> None:
    engine = ProfitEngine()
    result = engine.calculate(
        ProfitCalculationInput(
            request=CraftCalculationRequest(item_id="T4_BAG", city="Bridgewatch"),
            material_cost=1000,
            output_price=1500,
            rules=CraftRuleSet(city="Bridgewatch", crafting_fee=50, usage_fee=25, sales_tax=0.04),
        )
    )

    assert result.item_id == "T4_BAG"
    assert result.estimated_profit > 0