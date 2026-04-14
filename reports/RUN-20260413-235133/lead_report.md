## Scope
Update the `src/albion_factory/craftcalc/models.py` file to support Phase 1 and Phase 1.5 features for the Craft Calculator by adding new models and updating existing ones.

## Required Agents
- **Researcher**: To gather information on Pydantic models and best practices.
- **Coder**: To implement the changes in the `models.py` file.
- **Tester**: To ensure that the updates do not break existing functionality and that the new features work as expected.
- **Validator**: To review the code for adherence to coding standards and best practices.

## Constraints
- Do not break existing fields in the models.
- Use `pydantic.Field` where appropriate, especially for default values like dictionaries.

## Success Criteria
1. The `PlayerProfile` model is correctly implemented with all specified fields.
2. The `LocationContext` model is correctly implemented with all specified fields.
3. The `CraftPricePoint` model has been updated to include the new `source` and `owner_id` fields without breaking existing functionality.
4. The `CraftCalculationRequest` model has been updated to include the new `player_profile` and `location_context` fields without breaking existing functionality.
5. All changes are tested and validated for correctness and adherence to coding standards.

## Next Task
1. **Researcher**: Gather information on Pydantic models and best practices, specifically focusing on how to handle default values like dictionaries.
2. **Coder**: Implement the `PlayerProfile` and `LocationContext` models in `models.py`, ensuring that all fields are correctly defined and using `pydantic.Field` where appropriate.
3. **Coder**: Update the `CraftPricePoint` and `CraftCalculationRequest` models to include the new fields, ensuring that existing functionality is not broken.
4. **Tester**: Write tests for the new models and updates to ensure they work as expected without breaking existing functionality.
5. **Validator**: Review the code changes for adherence to coding standards and best practices, providing feedback for any necessary improvements.
6. Once all tasks are completed and reviewed, merge the changes into the main branch.