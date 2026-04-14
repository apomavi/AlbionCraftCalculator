## Scope
Update the `src/albion_factory/craftcalc/models.py` file to support Phase 1 and Phase 1.5 features for the Craft Calculator by adding new models and updating existing ones.

## Required Agents
- **Researcher**: To gather information on Pydantic models and best practices.
- **Coder**: To implement the changes in the `models.py` file.
- **Tester**: To ensure that the updates do not break existing functionality and that the new features work as expected.
- **Validator**: To review the code for adherence to coding standards and best practices.

## Constraints
- Do not break existing fields in the models.
- Use `pydantic.Field` where appropriate, especially for default factory values like dictionaries.

## Success Criteria
1. The `PlayerProfile` model is correctly implemented with all specified fields.
2. The `LocationContext` model is correctly implemented with all specified fields.
3. The `CraftPricePoint` model is updated to include the new `source` and `owner_id` fields without breaking existing functionality.
4. The `CraftCalculationRequest` model is updated to include the new `player_profile` and `location_context` fields without breaking existing functionality.
5. All changes are thoroughly tested and validated.

## Next Task
1. **Researcher**: Gather information on Pydantic models and best practices for implementing default factory values.
2. **Coder**: Implement the `PlayerProfile` and `LocationContext` models in `models.py`.
3. **Coder**: Update the `CraftPricePoint` and `CraftCalculationRequest` models with the new fields.
4. **Tester**: Write tests to ensure that the updates do not break existing functionality and that the new features work as expected.
5. **Validator**: Review the code for adherence to coding standards and best practices.
6. **Coder**: Make any necessary adjustments based on feedback from the Tester and Validator.
7. **Tester**: Re-run tests to confirm that all issues have been resolved.
8. **Validator**: Final review of the updated models.
9. **Coder**: Merge the changes into the main branch.

Please proceed with these tasks in sequence, ensuring that each step is completed before moving on to the next.