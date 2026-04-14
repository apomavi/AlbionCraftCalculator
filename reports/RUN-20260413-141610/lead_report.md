# Project Goal Implementation: Player Profile and Location Context Models

## Scope
Update `src/albion_factory/craftcalc/models.py` to support Phase 1 and Phase 1.5 features for the Craft Calculator.

## Required Agents
- **Researcher**: To gather requirements and understand existing codebase.
- **Coder**: To implement changes in `models.py`.
- **Tester**: To ensure all models are updated correctly with new fields and attributes.
- **Validator**: Confirm that no existing functionalities break due to changes.

## Constraints
1. Do not break existing fields.
2. Ensure proper use of `pydantic.Field` where necessary, especially for default values like dictionaries or other complex structures.

## Success Criteria
1. New `PlayerProfile` and `LocationContext` Pydantic models are created with the specified attributes.
2. Existing `CraftPricePoint` model is updated to include new fields.
3. Existing `CraftCalculationRequest` model is updated to include new nested fields.
4. All changes are verified by testers, ensuring no existing functionalities break.

## Next Step
1. **Researcher**: Gather necessary information and confirm the current codebase structure in `models.py`.
2. **Coder**: Begin implementing changes as per the requirements, ensuring adherence to constraints.
3. **Tester**: Prepare test cases for all models and fields to validate functionality after implementation.
4. **Validator**: Review the implemented changes to ensure that existing features remain unaltered.

## Detailed Plan

### Task 1: Research (Researcher)
- Understand current `models.py` structure.
- Verify existing `CraftPricePoint` and `CraftCalculationRequest` models.
- Document findings for Coder reference.

#### Next Step:
Send findings to Coder for implementation.

### Task 2: Implementation (Coder)

**Step 1: Create PlayerProfile Model**
```python
from pydantic import BaseModel, Field

class PlayerProfile(BaseModel):
    server: str = "europe"
    has_premium: bool = False
    global_crafting_discount: float = 0.0
    crafting_specs: dict[str, int] = Field(default_factory=dict)
    crafting_masteries: dict[str, int] = Field(default_factory=dict)
```

**Step 2: Create LocationContext Model**
```python
class LocationContext(BaseModel):
    city: str
    is_black_zone: bool = False
    hideout_level: int = 0
    hideout_biome_bonus: bool = False
    is_headquarters: bool = False
```

**Step 3: Update CraftPricePoint Model**
```python
class CraftPricePoint(BaseModel):
    # Existing fields...
    source: str = "AODP_PUBLIC"
    owner_id: str | None = None
```

**Step 4: Update CraftCalculationRequest Model**
```python
class CraftCalculationRequest(BaseModel):
    # Existing fields...
    player_profile: PlayerProfile | None = None
    location_context: LocationContext | None = None
```

#### Next Step:
Send updated models to Tester for testing.

### Task 3: Testing (Tester)
- Validate the new `PlayerProfile` and `LocationContext` models by creating instances.
- Test updates in `CraftPricePoint` and `CraftCalculationRequest` with new fields.
- Ensure no regression issues occur with existing functionalities.

#### Next Step:
Send test results to Validator for validation.

### Task 4: Validation (Validator)
- Review the implementation against all requirements.
- Confirm that changes do not alter existing features' behavior.
- Final confirmations and sign-off.

#### Next Step:
Deployment of updated code if all checks are successful.