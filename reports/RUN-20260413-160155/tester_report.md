- Created `PlayerProfile` model with appropriate fields.
- Created `LocationContext` model with appropriate fields.
- Updated `CraftPricePoint` model by adding `source` field.
- Updated `CraftCalculationRequest` model by adding `player_profile` and `location_context` fields.

Here is the updated content of src/albion_factory/craftcalc/models.py:

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional

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
    source: Optional[str] = Field(default=None, const=True)


class CraftRuleSet(BaseModel):
    city: str
    crafting_fee: float = 0.0
    sales_tax: float = 0.0
    usage_fee: float = 0.0
    resource_return_rate: float = 0.0
    focus_enabled: bool = False


class PlayerProfile(BaseModel):
    character_name: str
    level: int = Field(gt=0)
    gear_score: Optional[int] = None
    alliance_id: Optional[str] = None


class LocationContext(BaseModel):
    city: str
    region: Optional[str] = None
    stability: Optional[float] = None


class CraftCalculationRequest(BaseModel):
    item_id: str
    city: str
    quality: int | None = None
    use_focus: bool = False
    include_taxes: bool = True
    player_profile: Optional[PlayerProfile] = Field(default=None)
    location_context: Optional[LocationContext] = Field(default=None)


class CraftCalculationResult(BaseModel):
    item_id: str
    city: str
    estimated_input_cost: float = 0.0
    estimated_output_value: float = 0.0
    estimated_profit: float = 0.0
    profit_margin: float = 0.0
    break_even_price: float = 0.0
    notes: list[str] = Field(default_factory=list)