## Target Data
- `PlayerProfile` model (pydantic BaseModel) with fields: `server`, `has_premium`, `global_crafting_discount`, `crafting_specs`, `crafting_masteries`.
- `LocationContext` model (pydantic BaseModel) with fields: `city`, `is_black_zone`, `hideout_level`, `hideout_biome_bonus`, `is_headquarters`.
- Update existing `CraftPricePoint` model to include `source` and `owner_id` fields.
- Update existing `CraftCalculationRequest` model to include `player_profile` and `location_context` fields.

## Collected Data
```python
from pydantic import BaseModel, Field

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

class CraftCalculationRequest(BaseModel):
    item_id: str
    city: str
    quality: int | None = None
    use_focus: bool = False
    include_taxes: bool = True
    player_profile: PlayerProfile | None = None
    location_context: LocationContext | None = None
```

## Normalization Notes
- The `PlayerProfile` and `LocationContext` models were created as specified, using `pydantic.Field(default_factory=dict)` for dictionary fields.
- The existing `CraftPricePoint` and `CraftCalculationRequest` models were updated to include the new fields without breaking existing functionality.