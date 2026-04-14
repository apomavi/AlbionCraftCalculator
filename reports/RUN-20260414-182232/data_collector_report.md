```markdown
## Target Data
- Create `PlayerProfile` model (pydantic BaseModel) with specified fields and default values.
- Create `LocationContext` model (pydantic BaseModel) with specified fields and default values.
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
    # Existing fields...
    source: str = "AODP_PUBLIC"
    owner_id: str | None = None

class CraftCalculationRequest(BaseModel):
    # Existing fields...
    player_profile: PlayerProfile | None = None
    location_context: LocationContext | None = None
```

## Normalization Notes
- The `PlayerProfile` and `LocationContext` models were created with the specified fields and default values.
- The `CraftPricePoint` model was updated to include the new `source` and `owner_id` fields with appropriate default values.
- The `CraftCalculationRequest` model was updated to include the new `player_profile` and `location_context` fields with appropriate default values.
- Existing fields were not broken, and `pydantic.Field` was used where appropriate for default factory methods.
```