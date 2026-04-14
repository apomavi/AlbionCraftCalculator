# Scope

The scope of this task is to update the `src/albion_factory/craftcalc/models.py` file to support Phase 1 and Phase 1.5 features for the Craft Calculator. This involves creating two new models, `PlayerProfile` and `LocationContext`, as well as updating existing models `CraftPricePoint` and `CraftCalculationRequest`.

# Required Agents

- **Researcher**: To gather information on the current state of the `models.py` file and ensure compatibility with the new features.
- **Coder**: To implement the changes in the `models.py` file, including creating the new models and updating existing ones.
- **Tester**: To validate that the changes do not break existing functionality and that the new features work as expected.
- **Validator**: To review the code changes for adherence to coding standards and best practices.

# Constraints

1. Do not break existing fields in any of the models.
2. Use `pydantic.Field` where appropriate, especially for default values like dictionaries or lists.
3. Ensure that all new fields have sensible defaults where applicable.

# Success Criteria

1. The `PlayerProfile` model is correctly implemented with all specified fields and their respective types and defaults.
2. The `LocationContext` model is correctly implemented with all specified fields and their respective types and defaults.
3. The `CraftPricePoint` model has been updated to include the new `source` and `owner_id` fields without breaking existing functionality.
4. The `CraftCalculationRequest` model has been updated to include the new `player_profile` and `location_context` fields without breaking existing functionality.
5. All changes have been thoroughly tested to ensure they work as expected and do not introduce any regressions.
6. The code changes have been reviewed for adherence to coding standards and best practices.

# Next Step

1. **Researcher**: Begin by reviewing the current state of `models.py` to understand the existing models and their fields. Identify any potential conflicts or dependencies that need to be considered during the implementation of the new features.
2. **Coder**: Based on the research findings, start implementing the changes in the `models.py` file. Create the `PlayerProfile` and `LocationContext` models using Pydantic's `BaseModel`. Update the existing `CraftPricePoint` and `CraftCalculationRequest` models to include the new fields.
3. **Tester**: Once the code changes are implemented, begin testing the updated models to ensure that they work as expected without breaking any existing functionality. Pay special attention to edge cases and default values.
4. **Validator**: Review the code changes for adherence to coding standards and best practices. Ensure that all new fields have sensible defaults and that the use of `pydantic.Field` is appropriate where necessary.
5. Once all agents have completed their tasks, gather feedback and make any necessary adjustments before finalizing the implementation.

By following this structured approach, we can ensure that the updates to `models.py` are implemented correctly, tested thoroughly, and meet the required standards for quality and functionality.