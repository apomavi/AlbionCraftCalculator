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
    source: str = "AODP_PUBLIC"
    owner_id: str | None = None

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