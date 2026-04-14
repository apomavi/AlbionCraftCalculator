# Scope

The scope of this task is to update the `src/albion_factory/craftcalc/models.py` file to support Phase 1 and Phase 1.5 features for the Craft Calculator. This involves creating two new models, `PlayerProfile` and `LocationContext`, as well as updating existing models `CraftPricePoint` and `CraftCalculationRequest`.

# Required Agents

- **Researcher**: To gather information on the current state of the `models.py` file and ensure compatibility with the new features.
- **Coder**: To implement the changes in the `models.py` file, including creating the new models and updating existing ones.
- **Tester**: To test the updated models to ensure they work as expected without breaking existing functionality.
- **Validator**: To validate that the code adheres to the project's coding standards and best practices.

# Constraints

1. Do not break existing fields in any of the models.
2. Use `pydantic.Field` where appropriate, especially for default values like dictionaries or lists.
3. Ensure that all changes are backward compatible with existing features.

# Success Criteria

1. The `PlayerProfile` model is correctly implemented with all specified fields and default values.
2. The `LocationContext` model is correctly implemented with all specified fields and default values.
3. The `CraftPricePoint` model has been updated to include the new `source` and `owner_id` fields without breaking existing functionality.
4. The `CraftCalculationRequest` model has been updated to include the new `player_profile` and `location_context` fields without breaking existing functionality.
5. All changes have been tested and validated for correctness and backward compatibility.

# Next Step

1. **Researcher**: Begin by reviewing the current state of `models.py` to understand the existing models and their relationships. Identify any potential conflicts or dependencies that need to be addressed during the update.
2. **Coder**: Based on the research findings, start implementing the new models (`PlayerProfile` and `LocationContext`) and updating the existing models (`CraftPricePoint` and `CraftCalculationRequest`). Ensure that all fields are correctly defined and that default values are set appropriately using `pydantic.Field`.
3. **Tester**: Once the changes are implemented, write tests to validate that the new models work as expected and that the updated models do not break existing functionality.
4. **Validator**: Review the code changes for adherence to project standards and best practices. Ensure that all code is clean, well-documented, and follows the coding guidelines.

Once all steps are completed and validated, the task will be considered complete.