# Target Data

1. PlayerProfile model:
   - `server` (str, default "europe")
   - `has_premium` (bool, default False)
   - `global_crafting_discount` (float, default 0.0)
   - `crafting_specs` (dict[str, int])
   - `crafting_masteries` (dict[str, int])

2. LocationContext model:
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

# Collected Data

- PlayerProfile model data collected from various sources including user profiles and game settings.
- LocationContext model data collected from in-game city information and hideout details.
- CraftPricePoint model data collected from public APIs and databases providing item pricing information.
- CraftCalculationRequest model data collected from user requests for crafting profitability calculations.

# Normalization Notes

1. **PlayerProfile Model**:
   - `server`: Standardized to "europe" unless specified otherwise.
   - `has_premium`: Boolean values normalized to True or False.
   - `global_crafting_discount`: Float values normalized to a percentage format (e.g., 0.2 for 20%).
   - `crafting_specs` and `crafting_masteries`: Dictionary keys standardized to lowercase strings, ensuring consistent item names.

2. **LocationContext Model**:
   - `city`: City names standardized to proper case (e.g., "Lindera" instead of "lindera").
   - `is_black_zone`, `hideout_biome_bonus`, and `is_headquarters`: Boolean values normalized to True or False.
   - `hideout_level`: Integer values ensuring non-negative integers.

3. **CraftPricePoint Model**:
   - `source`: Default value set to "AODP_PUBLIC" unless specified otherwise.
   - `owner_id`: Optional string field, standardized to None if not provided.

4. **CraftCalculationRequest Model**:
   - `player_profile` and `location_context`: Optional fields, defaulting to None if not provided. Ensure that nested models are properly instantiated and validated.