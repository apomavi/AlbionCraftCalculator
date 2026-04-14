```markdown
# Data Collection Report

## Project Goal
- **REQ-0011: Player Profile and Location Context Models**

## Objective
Update `src/albion_factory/craftcalc/models.py` to support Phase 1 and Phase 1.5 features for the Craft Calculator.

## Required Changes
1. Create `PlayerProfile` model (pydantic BaseModel):
   - `server` (str, default "europe")
   - `has_premium` (bool, default False)
   - `global_crafting_discount` (float, default 0.0)
   - `crafting_specs` (dict[str, int])
   - `crafting_masteries` (dict[str, int])

2. Create `LocationContext` model (pydantic BaseModel):
   - `city` (str)
   - `is_black_zone` (bool, default False)
   - `hideout_level` (int, default 0)
   - `hideout_biome_bonus` (bool, default False)
   - `is_headquarters` (bool, default False)

3. Update existing `CraftPricePoint` model:
   - Add `source` (str, default "AODP_PUBLIC")
   - Add `owner_id` (str | None, default None)

4. Update existing `CraftCalculationRequest` model:
   - Add `player_profile` (PlayerProfile | None, default None)
   - Add `location_context` (LocationContext | None, default None)

## Target Data
- PlayerProfile Model:
  ```python
  from pydantic import BaseModel

  class PlayerProfile(BaseModel):
      server: str = "europe"
      has_premium: bool = False
      global_crafting_discount: float = 0.0
      crafting_specs: dict[str, int] = Field(default_factory=dict)
      crafting_masteries: dict[str, int] = Field(default_factory=dict)
  ```

- LocationContext Model:
  ```python
  from pydantic import BaseModel

  class LocationContext(BaseModel):
      city: str
      is_black_zone: bool = False
      hideout_level: int = 0
      hideout_biome_bonus: bool = False
      is_headquarters: bool = False
  ```

- Update `CraftPricePoint` Model:
  ```python
  from pydantic import BaseModel

  class CraftPricePoint(BaseModel):
      item_id: str
      city: str
      quality: int | None = None
      sell_price_min: float | None = None
      buy_price_max: float | None = None
      retrieved_at: str | None = None
      source: str = "AODP_PUBLIC"
      owner_id: str | None = None
  ```

- Update `CraftCalculationRequest` Model:
  ```python
  from pydantic import BaseModel

  class CraftCalculationRequest(BaseModel):
      item_id: str
      city: str
      quality: int | None = None
      use_focus: bool = False
      include_taxes: bool = True
      player_profile: PlayerProfile | None = None
      location_context: LocationContext | None = None
  ```

## Collected Data
- `PlayerProfile` model created with specified fields.
- `LocationContext` model created with specified fields.
- `CraftPricePoint` model updated to include `source` and `owner_id`.
- `CraftCalculationRequest` model updated to include `player_profile` and `location_context`.

## Normalization Notes
- Used Pydantic's `Field` for default factory settings (e.g., `default_factory=dict`) where applicable.
- Ensured backward compatibility by maintaining existing fields in the models.
```