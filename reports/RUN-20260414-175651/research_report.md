## Source Inventory
- `src/albion_factory/craftcalc/models.py` (content provided in previous turn)

## Findings
The existing `src/albion_factory/craftcalc/models.py` file needs to be updated to include two new Pydantic models: `PlayerProfile` and `LocationContext`. Additionally, the `CraftPricePoint` and `CraftCalculationRequest` models require new fields.

**New `PlayerProfile` model:**
- `server`: string, defaults to "europe".
- `has_premium`: boolean, defaults to `False`.
- `global_crafting_discount`: float, defaults to `0.0`.
- `crafting_specs`: dictionary with string keys and integer values.
- `crafting_masteries`: dictionary with string keys and integer values.

**New `LocationContext` model:**
- `city`: string.
- `is_black_zone`: boolean, defaults to `False`.
- `hideout_level`: integer, defaults to `0`.
- `hideout_biome_bonus`: boolean, defaults to `False`.
- `is_headquarters`: boolean, defaults to `False`.

**Updates to `CraftPricePoint` model:**
- Add `source`: string, defaults to "AODP_PUBLIC".
- Add `owner_id`: string or None, defaults to None.

**Updates to `CraftCalculationRequest` model:**
- Add `player_profile`: `PlayerProfile` or None, defaults to None.
- Add `location_context`: `LocationContext` or None, defaults to None.

The updates should adhere to Pydantic best practices, using `Field` where appropriate, especially for default factories for dictionaries.

## Constraints
- Do not break existing fields in the models.
- Use `pydantic.Field` for default factories (e.g., `default_factory=dict`).

## Implementation Notes
The following Python code will be the updated content for `src/albion_factory/craftcalc/models.py`. It incorporates the new models and fields as per the requirements.

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


class PlayerProfile(BaseModel):
    server: str = "europe"
    has_premium: bool = False
    global_crafting_discount: float = 0.0
    crafting_specs: dict[str, int] = Field(default_factory=dict)
    crafting_masteries: dict[str, int] = Field(default_factory=dict)


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
    source: str = "AODP_PUBLIC"  # Added field
    owner_id: str | None = None  # Added field


class CraftRuleSet(BaseModel):
    city: str
    crafting_fee: float = 0.0
    sales_tax: float = 0.0
    usage_fee: float = 0.0
    resource_return_rate: float = 0.0
    focus_enabled: bool = False


class CraftCalculationRequest(BaseModel):
    item_id: str
    city: str
    quality: int | None = None
    use_focus: bool = False
    include_taxes: bool = True
    player_profile: PlayerProfile | None = None  # Added field
    location_context: LocationContext | None = None  # Added field


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
- `src/albion_factory/craftcalc/models.py` (content read from repository)