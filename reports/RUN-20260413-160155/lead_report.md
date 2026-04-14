```json
{
  "Scope": "Update `src/albion_factory/craftcalc/models.py` to support Phase 1 and Phase 1.5 features for the Craft Calculator.",
  "Required Agents": [
    {
      "role": "Researcher",
      "tasks": ["Review existing `CraftPricePoint` and `CraftCalculationRequest` models.", "Identify fields that need updates according to the rules provided."]
    },
    {
      "role": "Coder",
      "tasks": [
        "Create `PlayerProfile` model with specified fields (including default values). Use `pydantic.Field` where necessary.",
        "Create `LocationContext` model with specified fields (including default values). Use `pydantic.Field` where necessary.",
        "Update existing `CraftPricePoint` model to include new fields (`source` and `owner_id`), ensuring no existing fields are broken.",
        "Update existing `CraftCalculationRequest` model to include new fields (`player_profile` and `location_context`), ensuring no existing fields are broken."
      ]
    },
    {
      "role": "Tester",
      "tasks": [
        "Write unit tests for `PlayerProfile` and `LocationContext` models to ensure correct behavior with default values.",
        "Verify that updates to `CraftPricePoint` model do not affect existing functionality.",
        "Validate that `CraftCalculationRequest` model correctly integrates `player_profile` and `location_context` fields, including handling of defaults."
      ]
    },
    {
      "role": "Validator",
      "tasks": [
        "Review code changes against the provided rules to ensure no existing fields are broken.",
        "Confirm that all added fields use `pydantic.Field` when necessary for default values or other attributes.",
        "Ensure that integration between `CraftCalculationRequest`, `PlayerProfile`, and `LocationContext` models works as expected."
      ]
    }
  ],
  "Constraints": [
    "Do not break existing fields in the models.",
    "Use `pydantic.Field` where appropriate (e.g., for setting default values)."
  ],
  "Success Criteria": [
    "`PlayerProfile` and `LocationContext` models are correctly implemented with all specified fields including default values.",
    "`CraftPricePoint` model is updated to include `source` and `owner_id` fields without breaking existing functionality.",
    "`CraftCalculationRequest` model is updated to include `player_profile` and `location_context` fields without breaking existing functionality.",
    "All unit tests pass successfully, ensuring correct behavior of new models and updates.",
    "Validator confirms that all constraints are adhered to."
  ],
  "Next Step": [
    "Coordinate with each agent to ensure tasks are completed on time."
  ]
}
```