### Task Breakdown

**Decision Document: DEC-0011 - Player Profile and Location Context Models**

---

#### Scope:
Implement changes to the `src/albion_factory/craftcalc/models.py` file to support Phase 1 and Phase 1.5 features for the Craft Calculator.

#### Required Agents:
- Researcher
- Coder
- Tester
- Validator

#### Constraints:
- Do not break existing fields in existing models.
- Use `pydantic.Field` where appropriate, specifically for default factories (e.g., `default_factory=dict`).

#### Success Criteria:
1. Successful creation of `PlayerProfile` and `LocationContext` Pydantic models with the specified fields.
2. Successful updates to the `CraftPricePoint` and `CraftCalculationRequest` models, including new fields with appropriate types and defaults.
3. Ensuring that all existing models retain their previous functionality and fields intact.
4. Comprehensive unit tests for the newly added features.
5. Validation of the entire codebase using static analysis tools.
6. Approval by a peer validator.

#### Next Step:
- **Researcher**: Review the current `src/albion_factory/craftcalc/models.py` file to understand existing models and ensure compatibility with new changes.
  - **Action Items**:
    1. Familiarize with the existing `CraftPricePoint`, `CraftCalculationRequest` models, including their existing fields and types.
    2. Ensure there are no breaking changes or conflicts with existing models.

- **Coder**: Implement the required changes to create new models and update existing ones.
  - **Action Items**:
    1. Create `PlayerProfile` model with specified default values.
    2. Create `LocationContext` model with specified default values and use of `pydantic.Field`.
    3. Update `CraftPricePoint` by adding `source` and `owner_id` fields with appropriate defaults, including using `pydantic.Field` for default factories if needed.
    4. Update `CraftCalculationRequest` to include `player_profile` and `location_context`.

- **Tester**: Write unit tests for the newly created models and updated existing ones.
  - **Action Items**:
    1. Develop comprehensive unit tests covering all fields in `PlayerProfile`, `LocationContext`, `CraftPricePoint`, and `CraftCalculationRequest`.
    2. Ensure test coverage includes default values, custom defaults, and edge cases.

- **Validator**: Validate the implementation against existing code standards and validate through static analysis tools.
  - **Action Items**:
    1. Review the entire codebase to ensure consistency with project standards.
    2. Perform a static analysis check using relevant tools (e.g., `pylint`, `mypy`) to identify any issues.

---