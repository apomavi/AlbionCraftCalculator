# Report

## Target Data:
- `PlayerProfile` model (pydantic BaseModel) with the following attributes:
  - `server` (str, default "europe")
  - `has_premium` (bool, default False)
  - `global_crafting_discount` (float, default 0.0)
  - `crafting_specs` (dict[str, int])
  - `crafting_masteries` (dict[str, int])

- `LocationContext` model (pydantic BaseModel) with the following attributes:
  - `city` (str)
  - `is_black_zone` (bool, default False)
  - `hideout_level` (int, default 0)
  - `hideout_biome_bonus` (bool, default False)
  - `is_headquarters` (bool, default False)

- Update existing `CraftPricePoint` model:
  - Adding `source` (str, default "AODP_PUBLIC")
  - Adding `owner_id` (str | None, default None)

- Update existing `CraftCalculationRequest` model:
  - Adding `player_profile` (PlayerProfile | None, default None)
  - Adding `location_context` (LocationContext | None, default None)

## Collected Data:

### Review of Current Models in `src/albion_factory/craftcalc/models.py`
After reviewing the current models in `src/albion_factory/craftcalc/models.py`, I identified the following existing models and their structure:

- **CraftPricePoint**: This model is used to represent pricing information for crafting items. The fields include:
  - `item_id` (str)
  - `price` (float)
  - `currency_type` (str)

- **CraftCalculationRequest**: This model encapsulates the data needed for crafting calculations. The existing fields include:
  - `item_id` (str)
  - `quantity` (int)

### Identified Dependencies and Potential Impacts
During the review, there were no immediate dependencies between the models that would be impacted by adding the new fields. However, it's essential to ensure that the integration of the new models (`PlayerProfile` and `LocationContext`) with existing models (`CraftPricePoint` and `CraftCalculationRequest`) follows Pydantic’s principles and does not disrupt current functionalities.

## Normalization Notes:
- Since there are no direct dependencies between the new models and existing ones, we'll use the default values provided for flexibility in how these attributes can be interacted with across different contexts.
- For fields that require a dictionary as a type (`crafting_specs` and `crafting_masteries`), we will use Pydantic’s `default_factory=dict` to ensure default empty dictionaries are used when no specific value is provided. This approach aligns with best practices for handling mutable types in immutable defaults.

### Next Steps:
1. **Implement the New Models (`PlayerProfile` and `LocationContext`).**
2. **Update Existing Models (`CraftPricePoint` and `CraftCalculationRequest`) to Include New Fields.**
3. **Test Thoroughly to Ensure No Breaks in Existing Functionality.**

By following this approach, we will ensure that all changes align with the project goals without disrupting existing features.

---

**Status:** Ready for Implementation of Models