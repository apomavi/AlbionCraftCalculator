## Target Data

- `PlayerProfile` model (pydantic BaseModel):
  - `server` (str, default "europe")
  - `has_premium` (bool, default False)
  - `global_crafting_discount` (float, default 0.0)
  - `crafting_specs` (dict[str, int])
  - `crafting_masteries` (dict[str, int])

- `LocationContext` model (pydantic BaseModel):
  - `city` (str)
  - `is_black_zone` (bool, default False)
  - `hideout_level` (int, default 0)
  - `hideout_biome_bonus` (bool, default False)
  - `is_headquarters` (bool, default False)

- Update existing `CraftPricePoint` model:
  - Add `source` (str, default "AODP_PUBLIC")
  - Add `owner_id` (str | None, default None)

- Update existing `CraftCalculationRequest` model:
  - Add `player_profile` (PlayerProfile | None, default None)
  - Add `location_context` (LocationContext | None, default None)

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

# Assuming CraftPricePoint and CraftCalculationRequest are already defined in models.py
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

- The `PlayerProfile` and `LocationContext` models are created as pydantic BaseModel classes with the specified fields and default values.
- For dynamic default values like dictionaries (`crafting_specs` and `crafting_masteries`), `Field(default_factory=dict)` is used to ensure each instance has its own separate dictionary.
- The existing `CraftPricePoint` and `CraftCalculationRequest` models are updated to include the new fields with appropriate default values.