from albion_factory.craftcalc.models import CraftRecipe, CraftRecipeIngredient
from albion_factory.craftcalc.recipe_resolver import RecipeResolver


def test_recipe_resolver_missing_item() -> None:
    resolver = RecipeResolver(recipes=[])
    result = resolver.resolve("T4_BAG")

    assert result.recipe is None
    assert result.missing_items == ["T4_BAG"]
    assert result.cycle_detected is False


def test_recipe_resolver_basic_recipe() -> None:
    resolver = RecipeResolver(
        recipes=[
            CraftRecipe(
                recipe_id="recipe-bag",
                output_item_id="T4_BAG",
                output_item_name="T4 Bag",
                ingredients=[
                    CraftRecipeIngredient(item_id="T4_CLOTH", item_name="T4 Cloth", quantity=4),
                ],
            )
        ]
    )

    result = resolver.resolve("T4_BAG")

    assert result.recipe is not None
    assert result.recipe.output_item_id == "T4_BAG"