## Scope
Update the `src/albion_factory/craftcalc/models.py` file to support Phase 1 and Phase 1.5 features for the Craft Calculator by adding new models (`PlayerProfile` and `LocationContext`) and updating existing models (`CraftPricePoint` and `CraftCalculationRequest`).

## Required Agents
- **Researcher**: To gather information on Pydantic models and ensure compatibility with existing code.
- **Coder**: To implement the changes in the `models.py` file.
- **Tester**: To validate the new models and updated fields for functionality and correctness.
- **Validator**: To review the implementation against the provided rules and ensure no existing fields are broken.

## Constraints
1. Do not break any existing fields in the models.
2. Use `pydantic.Field` where appropriate, especially for default values that require factory functions (e.g., `default_factory=dict`).

## Success Criteria
1. The `PlayerProfile` model is correctly implemented with all specified fields and default values.
2. The `LocationContext` model is correctly implemented with all specified fields and default values.
3. The `CraftPricePoint` model is updated to include the new `source` and `owner_id` fields without breaking existing functionality.
4. The `CraftCalculationRequest` model is updated to include the new `player_profile` and `location_context` fields without breaking existing functionality.
5. All changes are tested for correctness and compatibility with existing code.

## Next Task
1. **Researcher**: Gather detailed information on Pydantic models, specifically focusing on how to implement default values using `pydantic.Field`.
2. **Coder**: Begin implementing the new models (`PlayerProfile` and `LocationContext`) and updating the existing models (`CraftPricePoint` and `CraftCalculationRequest`) based on the gathered information.
3. **Tester**: Prepare test cases for the new models and updated fields to ensure they function as expected without breaking existing functionality.
4. **Validator**: Review the implementation against the provided rules and constraints to ensure compliance.

Once these tasks are completed, move on to the next phase of testing and validation.