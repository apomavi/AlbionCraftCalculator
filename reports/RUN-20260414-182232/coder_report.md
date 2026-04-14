## Target Files
src/albion_factory/craftcalc/models.py

## Planned Changes
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

## Applied Changes
- The `PlayerProfile` and `LocationContext` models were already defined in the file.
- The `CraftPricePoint` model was updated to include the new `source` and `owner_id` fields with appropriate default values.
- The `CraftCalculationRequest` model was updated to include the new `player_profile` and `location_context` fields with appropriate default values.

## Remaining Risks
- Ensure that the existing fields in the models are not broken by these changes.