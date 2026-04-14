### Target Data

- **Models to be created**:
  - `PlayerProfile`
  - `LocationContext`

- **Updates to existing models**:
  - `CraftPricePoint` (add `source` and `owner_id`)
  - `CraftCalculationRequest` (add `player_profile` and `location_context`)

### Collected Data

1. **Existing `CraftPricePoint` Model Analysis**:
   ```python
   from pydantic import BaseModel, Field

   class CraftPricePoint(BaseModel):
       owner_id: str | None = None # Note: added owner_id and source from legacy AODP_PUBLIC
       source: str = "AODP_PUBLIC"
   ```

2. **Existing `CraftCalculationRequest` Model Analysis**:
   ```python
   from pydantic import BaseModel, Field

   class CraftCalculationRequest(BaseModel):
       player_profile: PlayerProfile | None = None # type: ignore
       location_context: LocationContext | None = None # type: ignore
   ```

### Normalization Notes

1. **PlayerProfile Model**:
   - `server`: Added as per requirement with default value "europe".
   - `has_premium`: Added as a boolean field with default False.
   - `global_crafting_discount`: Added as a float field with default 0.0.
   - `crafting_specs` and `crafting_masteries`: Both are added using `Field(default_factory=dict)` to ensure they are initialized dicts.

2. **LocationContext Model**:
   - `city`: Added with no default, it is required for location context.
   - `is_black_zone`: Optional boolean field with default False.
   - `hideout_level`: Integer field with default 0.
   - `hideout_biome_bonus`: Optional boolean field, default False.
   - `is_headquarters`: Optional boolean field, default False.

3. **CraftPricePoint Model**:
   - The existing implementation already includes the required fields `source` and `owner_id`. No modifications are necessary as they align with the project requirements.

4. **CraftCalculationRequest Model**:
   - Updated placeholders for both `player_profile` and `location_context` to reflect the newly created models.
   - These should be correctly referenced once the `PlayerProfile` and `LocationContext` models are added in the same file.

This implementation adheres to rules provided, maintains existing fields, and leverages Pydantic's features as required.