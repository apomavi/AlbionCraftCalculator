from __future__ import annotations

from dataclasses import dataclass, field

from albion_factory.craftcalc.models import CraftRecipe


@dataclass
class RecipeResolutionResult:
    item_id: str
    recipe: CraftRecipe | None
    missing_items: list[str] = field(default_factory=list)
    visited_items: list[str] = field(default_factory=list)
    cycle_detected: bool = False


class RecipeResolver:
    """Resolves recipe trees for craft calculator foundations.

    This is an initial skeleton for Phase 2. It provides:
    - item -> recipe lookup
    - recursive traversal
    - missing item tracking
    - cycle detection
    """

    def __init__(self, recipes: list[CraftRecipe]) -> None:
        self._recipes_by_output = {recipe.output_item_id: recipe for recipe in recipes}

    def get_recipe(self, item_id: str) -> CraftRecipe | None:
        return self._recipes_by_output.get(item_id)

    def resolve(self, item_id: str) -> RecipeResolutionResult:
        return self._resolve(item_id=item_id, active_stack=[])

    def _resolve(self, item_id: str, active_stack: list[str]) -> RecipeResolutionResult:
        if item_id in active_stack:
            return RecipeResolutionResult(
                item_id=item_id,
                recipe=None,
                missing_items=[],
                visited_items=active_stack + [item_id],
                cycle_detected=True,
            )

        recipe = self.get_recipe(item_id)
        if recipe is None:
            return RecipeResolutionResult(
                item_id=item_id,
                recipe=None,
                missing_items=[item_id],
                visited_items=active_stack + [item_id],
                cycle_detected=False,
            )

        visited = active_stack + [item_id]
        missing_items: list[str] = []
        cycle_detected = False

        for ingredient in recipe.ingredients:
            child = self._resolve(ingredient.item_id, visited)
            missing_items.extend(child.missing_items)
            cycle_detected = cycle_detected or child.cycle_detected

        return RecipeResolutionResult(
            item_id=item_id,
            recipe=recipe,
            missing_items=sorted(set(missing_items)),
            visited_items=visited,
            cycle_detected=cycle_detected,
        )