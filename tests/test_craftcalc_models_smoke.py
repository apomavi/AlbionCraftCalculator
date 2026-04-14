from albion_factory.craftcalc import CraftCalculationRequest, CraftCalculationResult


def test_craftcalc_models_importable() -> None:
    request = CraftCalculationRequest(item_id="T4_BAG", city="Bridgewatch")
    result = CraftCalculationResult(item_id="T4_BAG", city="Bridgewatch")

    assert request.item_id == "T4_BAG"
    assert result.city == "Bridgewatch"