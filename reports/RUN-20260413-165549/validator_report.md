## Verdict
FAIL

# Evidence

The `src/albion_factory/craftcalc/models.py` file does not contain the necessary models and updates for Phase 1 and Phase 1.5 features as specified in # REQ-0011: Player Profile and Location Context Models.

# Feedback

The current implementation of `src/albion_factory/craftcalc/models.py` is missing the following:

1. **PlayerProfile model**:
   - `server` (str, default "europe")
   - `has_premium` (bool, default False)
   - `global_crafting_discount` (float, default 0.0)
   - `crafting_specs` (dict[str, int])
   - `crafting_masteries` (dict[str, int])

2. **LocationContext model**:
   - `city` (str)
   - `is_black_zone` (bool, default False)
   - `hideout_level` (int, default 0)
   - `hideout_biome_bonus` (bool, default False)
   - `is_headquarters` (bool, default False)

3. **Updates to existing models**:
   - **CraftPricePoint model**:
     - Add `source` (str, default "AODP_PUBLIC")
     - Add `owner_id` (str | None, default None)
   
   - **CraftCalculationRequest model**:
     - Add `player_profile` (PlayerProfile | None, default None)
     - Add `location_context` (LocationContext | None, default None)

# Next Steps

1. Implement the missing models and updates in `src/albion_factory/craftcalc/models.py`.
2. Ensure that all fields are properly defined with their respective types and default values.
3. Verify that the updated file meets the requirements specified in # REQ-0011: Player Profile and Location Context Models.
4. Re-run the tests to confirm that the changes have been correctly implemented.

# Example Implementation

```python
from pydantic import BaseModel, Field
from typing import Dict, Optional

class PlayerProfile(BaseModel):
    server: str = "europe"
    has_premium: bool = False
    global_crafting_discount: float = 0.0
    crafting_specs: Dict[str, int] = {}
    crafting_masteries: Dict[str, int] = {}

class LocationContext(BaseModel):
    city: str
    is_black_zone: bool = False
    hideout_level: int = 0
    hideout_biome_bonus: bool = False
    is_headquarters: bool = False

class CraftPricePoint(BaseModel):
    source: str = "AODP_PUBLIC"
    owner_id: Optional[str] = None
    # Existing fields...

class CraftCalculationRequest(BaseModel):
    player_profile: Optional[PlayerProfile] = None
    location_context: Optional[LocationContext] = None
    # Existing fields...
```

Please ensure that the implementation aligns with the requirements and re-run the tests to validate the changes.

## Evidence Used
No structured evidence provided

## Risks
Validator returned unstructured risks section

## Required Fixes
Provide validator output in required contract format

## Feedback Target
none

## Feedback Reason
Validator output did not follow required structured format

## Commit Ready
NO
