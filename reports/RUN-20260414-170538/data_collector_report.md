## Target Data
- `PlayerProfile` model (pydantic BaseModel) with fields: `server`, `has_premium`, `global_crafting_discount`, `crafting_specs`, `crafting_masteries`.
- `LocationContext` model (pydantic BaseModel) with fields: `city`, `is_black_zone`, `hideout_level`, `hideout_biome_bonus`, `is_headquarters`.
- Update `CraftPricePoint` model to include fields: `source`, `owner_id`.
- Update `CraftCalculationRequest` model to include fields: `player_profile`, `location_context`.

## Final Answer
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