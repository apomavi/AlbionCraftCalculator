## Source Inventory
- `src/albion_factory/craftcalc/models.py`

## Findings
The objective is to update `src/albion_factory/craftcalc/models.py` to support Phase 1 and Phase 1.5 features for the Craft Calculator by adding new models and modifying existing ones.

**New Models to Create:**

1.  **`PlayerProfile` model:**
    *   `server` (str, default "europe")
    *   `has_premium` (bool, default False)
    *   `global_crafting_discount` (float, default 0.0)
    *   `crafting_specs` (dict[str, int])
    *   `crafting_masteries` (dict[str, int])

2.  **`LocationContext` model:**
    *   `city` (str)
    *   `is_black_zone` (bool, default False)
    *   `hideout_level` (int, default 0)
    *   `hideout_biome_bonus` (bool, default False)
    *   `is_headquarters` (bool, default False)

**Existing Models to Update:**

1.  **`CraftPricePoint` model:**
    *   Add `source` (str, default "AODP_PUBLIC")
    *   Add `owner_id` (str | None, default None)

2.  **`CraftCalculationRequest` model:**
    *   Add `player_profile` (PlayerProfile | None, default None)
    *   Add `location_context` (LocationContext | None, default None)

**Rules to Follow:**
*   Do not break existing fields.
*   Use `pydantic.Field` where appropriate (e.g., for `default_factory=dict`).

## Constraints
- The code must be valid Python and Pydantic.
- Existing fields in `CraftPricePoint` and `CraftCalculationRequest` must be preserved.

## Implementation Notes
The following Python code snippet represents the updated `src/albion_factory/craftcalc/models.py` file incorporating all the required changes.

```python
from __future__ import annotations

from pydantic import BaseModel, Field


class CraftRecipeIngredient(BaseModel):
    item_id: str
    item_name: str
    quantity: float = Field(gt=0)


class CraftRecipe(BaseModel):
    recipe_id: str
    output_item_id: str
    output_item_name: str
    output_quantity: float = Field(default=1, gt=0)
    ingredients: list[CraftRecipeIngredient] = Field(default_factory=list)


# New PlayerProfile model
class PlayerProfile(BaseModel):
    server: str = "europe"
    has_premium: bool = False
    global_crafting_discount: float = 0.0
    crafting_specs: dict[str, int] = Field(default_factory=dict)
    crafting_masteries: dict[str, int] = Field(default_factory=dict)


# New LocationContext model
class LocationContext(BaseModel):
    city: str
    is_black_zone: bool = False
    hideout_level: int = 0
    hideout_biome_bonus: bool = False
    is_headquarters: bool = False


class CraftPricePoint(BaseModel):
    item_id: str
    city: str
    quality: int | None = None
    sell_price_min: float | None = None
    buy_price_max: float | None = None
    retrieved_at: str | None = None
    # Added fields
    source: str = "AODP_PUBLIC"
    owner_id: str | None = None


class CraftCalculationRequest(BaseModel):
    item_id: str
    city: str
    quality: int | None = None
    use_focus: bool = False
    include_taxes: bool = True
    # Added fields
    player_profile: PlayerProfile | None = None
    location_context: LocationContext | None = None


class CraftCalculationResult(BaseModel):
    item_id: str
    city: str
    estimated_input_cost: float = 0.0
    estimated_output_value: float = 0.0
    estimated_profit: float = 0.0
    profit_margin: float = 0.0
    break_even_price: float = 0.0
    notes: list[str] = Field(default_factory=list)

```

## Sources
- `src/albion_factory/craftcalc/models.py` (Content analyzed to ensure backward compatibility and apply updates)