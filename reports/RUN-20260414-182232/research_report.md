## Source Inventory
- `src/albion_factory/craftcalc/models.py`

## Findings
- The existing `PlayerProfile` and `LocationContext` models are already defined in the file.
- The `CraftPricePoint` model needs to be updated with `source` and `owner_id` fields.
- The `CraftCalculationRequest` model needs to be updated with `player_profile` and `location_context` fields.

## Constraints
- Do not break existing fields.
- Use `pydantic.Field` where appropriate (e.g., for `default_factory=dict`).

## Implementation Notes
1. Ensure that the `PlayerProfile` and `LocationContext` models are correctly defined with the specified fields and default values.
2. Update the `CraftPricePoint` model to include the new `source` and `owner_id` fields with appropriate default values.
3. Update the `CraftCalculationRequest` model to include the new `player_profile` and `location_context` fields with appropriate default values.

## Sources
- `src/albion_factory/craftcalc/models.py`