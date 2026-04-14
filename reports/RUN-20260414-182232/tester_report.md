## Commands
- read_repo_file with path "src/albion_factory/craftcalc/models.py"

## Evidence
The file `src/albion_factory/craftcalc/models.py` contains the following models:

1. **PlayerProfile**:
   - `server` (str, default "europe")
   - `has_premium` (bool, default False)
   - `global_crafting_discount` (float, default 0.0)
   - `crafting_specs` (dict[str, int])
   - `crafting_masteries` (dict[str, int])

2. **LocationContext**:
   - `city` (str)
   - `is_black_zone` (bool, default False)
   - `hideout_level` (int, default 0)
   - `hideout_biome_bonus` (bool, default False)
   - `is_headquarters` (bool, default False)

3. **CraftPricePoint**:
   - Existing fields plus new fields:
     - `source` (str, default "AODP_PUBLIC")
     - `owner_id` (str | None, default None)

4. **CraftCalculationRequest**:
   - Existing fields plus new fields:
     - `player_profile` (PlayerProfile | None, default None)
     - `location_context` (LocationContext | None, default None)

## Findings
- The `PlayerProfile` and `LocationContext` models are correctly defined.
- The `CraftPricePoint` model has been updated with the new fields `source` and `owner_id`.
- The `CraftCalculationRequest` model has been updated with the new fields `player_profile` and `location_context`.

## Verdict
The changes meet the requirements specified in Project Goal # REQ-0011.