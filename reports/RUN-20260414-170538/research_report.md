## Source Inventory
The following files and web resources were consulted:
- `src/albion_factory/craftcalc/models.py`: Provided the existing structure of the Pydantic models.
- Pydantic Documentation (via `smart_research`): Confirmed the usage of `pydantic.Field` and `default_factory` for setting default values, particularly for dictionaries.

## Findings
1.  **Pydantic `Field` and `default_factory`**: The `pydantic.Field` function allows for customization of model fields, including setting default values. For mutable default values like dictionaries, `default_factory` should be used. For example, `crafting_specs: dict[str, int] = Field(default_factory=dict)` ensures that a new dictionary is created for each instance if no value is provided.
2.  **Model Structure**: The existing `models.py` file uses `pydantic.BaseModel` and `pydantic.Field`. New models (`PlayerProfile`, `LocationContext`) can be created as `BaseModel` subclasses, and existing models (`CraftPricePoint`, `CraftCalculationRequest`) can be updated by adding new fields.
3.  **Default Values**: The requirements specify default values for several fields:
    *   `PlayerProfile`: `server` (str, default "europe"), `has_premium` (bool, default False), `global_crafting_discount` (float, default 0.0), `crafting_specs` (dict[str, int]), `crafting_masteries` (dict[str, int]). For `crafting_specs` and `crafting_masteries`, `default_factory=dict` should be used.
    *   `LocationContext`: `is_black_zone` (bool, default False), `hideout_level` (int, default 0), `hideout_biome_bonus` (bool, default False), `is_headquarters` (bool, default False).
    *   `CraftPricePoint`: `source` (str, default "AODP_PUBLIC").
    *   `CraftCalculationRequest`: `player_profile` (PlayerProfile | None, default None), `location_context` (LocationContext | None, default None).

## Constraints
1.  **No Breaking Changes**: Existing fields in `CraftPricePoint` and `CraftCalculationRequest` must remain functional.
2.  **`pydantic.Field` Usage**: Use `pydantic.Field` where appropriate, especially for `default_factory=dict`.

## Implementation Notes
The `src/albion_factory/craftcalc/models.py` file needs to be updated as follows:
1.  Import `Field` from `pydantic` if not already present (it is).
2.  Define the `PlayerProfile` model with the specified fields and default values, using `default_factory=dict` for `crafting_specs` and `crafting_masteries`.
3.  Define the `LocationContext` model with the specified fields and default values.
4.  Add `source` and `owner_id` to the `CraftPricePoint` model.
5.  Add `player_profile` and `location_context` to the `CraftCalculationRequest` model.
6.  Ensure type hints are correct, including `dict[str, int]` and `str | None`.

## Sources
- `src/albion_factory/craftcalc/models.py` (Content provided by `read_repo_file`)
- Pydantic Documentation on Fields: https://pydantic.dev/docs/validation/latest/concepts/fields/ (Accessed via `smart_research`)
- Pydantic Documentation on `default_factory`: https://pydantic.dev/docs/validation/latest/api/pydantic/fields/ (Accessed via `smart_research`)
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


class CraftPricePoint(BaseModel):
    item_id: str
    city: str
    quality: int | None = None
    sell_price_min: float | None = None
    buy_price_max: float | None = None
    retrieved_at: str | None = None
    # Added fields for Phase 1 and 1.5
    source: str = Field(default="AODP_PUBLIC")
    owner_id: str | None = Field(default=None)


class CraftRuleSet(BaseModel):
    city: str
    crafting_fee: float = 0.0
    sales_tax: float = 0.0
    usage_fee: float = 0.0
    resource_return_rate: float = 0.0
    focus_enabled: bool = False

# New model for Player Profile
class PlayerProfile(BaseModel):
    server: str = Field(default="europe")
    has_premium: bool = Field(default=False)
    global_crafting_discount: float = Field(default=0.0)
    crafting_specs: dict[str, int] = Field(default_factory=dict)
    crafting_masteries: dict[str, int] = Field(default_factory=dict)

# New model for Location Context
class LocationContext(BaseModel):
    city: str
    is_black_zone: bool = Field(default=False)
    hideout_level: int = Field(default=0)
    hideout_biome_bonus: bool = Field(default=False)
    is_headquarters: bool = Field(default=False)


class CraftCalculationRequest(BaseModel):
    item_id: str
    city: str
    quality: int | None = None
    use_focus: bool = False
    include_taxes: bool = True
    # Added fields for Phase 1 and 1.5
    player_profile: PlayerProfile | None = Field(default=None)
    location_context: LocationContext | None = Field(default=None)


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