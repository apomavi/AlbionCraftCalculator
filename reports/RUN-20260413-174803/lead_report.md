## Scope
Update the `src/albion_factory/craftcalc/models.py` file to support Phase 1 and Phase 1.5 features for the Craft Calculator by adding new models (`PlayerProfile` and `LocationContext`) and updating existing models (`CraftPricePoint` and `CraftCalculationRequest`).

## Required Agents
- **Researcher**: To gather information on Pydantic models and ensure compatibility with existing code.
- **Coder**: To implement the changes in the `models.py` file.
- **Tester**: To verify that the new models and updates do not break existing functionality.
- **Validator**: To validate the implementation against the provided requirements.

## Constraints
- Do not break existing fields in any of the models.
- Use `pydantic.Field` where appropriate, especially for default values like dictionaries.

## Success Criteria
1. The `PlayerProfile` model is correctly implemented with all specified fields and default values.
2. The `LocationContext` model is correctly implemented with all specified fields and default values.
3. The `CraftPricePoint` model is updated to include the new `source` and `owner_id` fields without breaking existing functionality.
4. The `CraftCalculationRequest` model is updated to include the new `player_profile` and `location_context` fields without breaking existing functionality.
5. All changes are tested and validated to ensure they meet the requirements and do not introduce any regressions.

## Next Task
1. **Researcher**: Gather detailed information on Pydantic models, especially regarding default values for dictionaries, and review the current implementation of `models.py`.
2. **Coder**: Implement the new models (`PlayerProfile` and `LocationContext`) and update the existing models (`CraftPricePoint` and `CraftCalculationRequest`) based on the requirements.
3. **Tester**: Write unit tests to verify that the new models and updates do not break existing functionality.
4. **Validator**: Validate the implementation against the provided requirements and ensure all changes are correctly implemented.

Once these tasks are completed, the updated models will be ready for integration into the main codebase.