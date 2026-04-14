### Scope:
Update `src/albion_factory/craftcalc/models.py` to support Phase 1 and Phase 1.5 features for the Craft Calculator.

### Required Agents:
- **Researcher**: To verify requirements and ensure no breaking changes.
- **Coder**: To implement the required changes in the models.
- **Tester**: To test the new functionality without affecting existing ones.
- **Validator**: To review code changes for adherence to standards and best practices.

### Constraints:
- No breaking changes to existing fields.
- Use `pydantic.Field` where appropriate (e.g., for default_factory=dict).

### Success Criteria:
1. `PlayerProfile` model is correctly created with all specified fields.
2. `LocationContext` model is correctly created with all specified fields.
3. `CraftPricePoint` model is updated with new fields without breaking existing ones.
4. `CraftCalculationRequest` model is updated with new fields without breaking existing ones.
5. All changes are tested and validated to ensure no regression.

### Next Steps:

1. **Researcher**:
   - Verify the current models (`CraftPricePoint` and `CraftCalculationRequest`) to understand their existing structure and behaviors.
   - Confirm that no field names or functionalities will be broken by these changes.

2. **Coder**:
   - Create the `PlayerProfile` model in `models.py` with the specified fields using Pydantic's `BaseModel`.
   - Create the `LocationContext` model in `models.py` with the specified fields using Pydantic's `BaseModel`.
   - Update the `CraftPricePoint` model to include the new fields (`source`, `owner_id`) while ensuring backward compatibility.
   - Update the `CraftCalculationRequest` model to include the new fields (`player_profile`, `location_context`) while ensuring backward compatibility.

3. **Tester**:
   - Write thorough unit tests for the changes in each model.
   - Ensure that existing functionalities are not impacted and all new functionalities work as expected.

4. **Validator**:
   - Review code changes to ensure they follow coding standards and best practices.
   - Verify that `pydantic.Field` is used correctly where required.
   - Finalize the validation report with any necessary corrections or feedback.

5. **Orchestrator (You)**:
   - Once all tasks are completed, coordinate a code review session with the team to finalize changes.
   - Address any feedback from the testing and validation phases.
   - Merge the changes into the main branch after approval.
   - Prepare for any additional tasks or follow-up based on integration test results.

---

This breakdown ensures that all aspects of the task are covered, and each step is well-defined with clear responsibilities.