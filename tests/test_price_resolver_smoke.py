from albion_factory.craftcalc.models import CraftPricePoint
from albion_factory.craftcalc.price_resolver import PriceResolver


def test_price_resolver_sell_side() -> None:
    resolver = PriceResolver(
        prices=[
            CraftPricePoint(item_id="T4_BAG", city="Bridgewatch", sell_price_min=1200),
        ]
    )

    result = resolver.resolve("T4_BAG", "Bridgewatch")

    assert result.selected_price == 1200
    assert result.selected_side == "sell"
    assert result.used_fallback is False


def test_price_resolver_fallback_to_buy() -> None:
    resolver = PriceResolver(
        prices=[
            CraftPricePoint(item_id="T4_BAG", city="Bridgewatch", buy_price_max=900),
        ]
    )

    result = resolver.resolve("T4_BAG", "Bridgewatch", prefer_buy_order=False)

    assert result.selected_price == 900
    assert result.selected_side == "buy"
    assert result.used_fallback is True