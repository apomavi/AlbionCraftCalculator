from albion_factory.craftcalc.comparison_engine import ComparisonEngine


def test_compare_buy_vs_craft() -> None:
    engine = ComparisonEngine()
    result = engine.compare_buy_vs_craft(
        item_id="T4_BAG",
        city="Bridgewatch",
        craft_cost=1000,
        buy_cost=1200,
    )

    assert result.preferred_action == "craft"
    assert result.savings == 200


def test_compare_cities() -> None:
    engine = ComparisonEngine()
    result = engine.compare_cities(
        item_id="T4_BAG",
        city_prices={"Bridgewatch": 1200, "Martlock": 1100},
    )

    assert result.cheapest_city == "Martlock"


def test_compare_refine_craft_sell_chain() -> None:
    engine = ComparisonEngine()
    result = engine.compare_refine_craft_sell_chain(
        chain_id="chain-1",
        step_costs=[100, 150, 50],
        sell_value=400,
    )

    assert result.net_profit == 100


def test_cheapest_input_chain() -> None:
    engine = ComparisonEngine()
    result = engine.cheapest_input_chain(
        item_id="T4_BAG",
        candidate_inputs={"cloth": 200, "leather": 150},
    )

    assert list(result.chosen_inputs.keys())[0] == "leather"