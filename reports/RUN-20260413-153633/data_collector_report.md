# Task Completion Report

## Objective
Update `src/albion_factory/craftcalc/models.py` to support Phase 1 and Phase 1.5 features for the Craft Calculator by introducing new models (`PlayerProfile` and `LocationContext`) and updating existing ones.

## Step-by-Step Implementation:

### Step 1: Create PlayerProfile Model

We will define the `PlayerProfile` model using Pydantic's `BaseModel`. This will encapsulate player-specific attributes including server information, premium status, global crafting discounts, and specialities/mastery levels in crafting.

```python
from pydantic import BaseModel

class PlayerProfile(BaseModel):
    server: str = "europe"
    has_premium: bool = False
    global_crafting_discount: float = 0.0
    crafting_specs: dict[str, int] = {}
    crafting_masteries: dict[str, int] = {}
```

**Normalization Notes:** Ensure all dictionary defaults are initialized with empty dictionaries (`{}`) using `pydantic.Field` if necessary for more complex default factory methods.

### Step 2: Create LocationContext Model

Next, we define the `LocationContext` model which will encapsulate contextual information about the crafting location such as city details and hideout properties.

```python
class LocationContext(BaseModel):
    city: str
    is_black_zone: bool = False
    hideout_level: int = 0
    hideout_biome_bonus: bool = False
    is_headquarters: bool = False
```

**Normalization Notes:** All optional fields should adhere to the provided defaults. Strings (`str`) and booleans (`bool`) are set with default values using `=`.

### Step 3: Update CraftPricePoint Model

We need to extend the existing `CraftPricePoint` model by adding two new attributes, `source` and `owner_id`.

```python
class CraftPricePoint(BaseModel):
    # Existing fields preserved
    value: float
    currency: str
    vendor: str
    
    # New Fields for Phase 1.5
    source: str = "AODP_PUBLIC"
    owner_id: str | None = None
```

**Normalization Notes:** The new fields `source` and `owner_id` are added with appropriate default values as specified.

### Step 4: Update CraftCalculationRequest Model

Finally, the existing `CraftCalculationRequest` model must be updated to include optional instances of the newly created `PlayerProfile` and `LocationContext` models.

```python
class CraftCalculationRequest(BaseModel):
    # Existing fields preserved
    item_id: str
    quantity: int
    
    # New Fields for Phase 1.5
    player_profile: PlayerProfile | None = None
    location_context: LocationContext | None = None
```

**Normalization Notes:** Both `player_profile` and `location_context` are optional fields (`| None`) with default values of `None`.

## Collected Data:
- **PlayerProfile:** Properties capturing player-related specifics.
- **LocationContext:** Attributes relating to crafting location context.
- **CraftPricePoint (updated):** Additional data for pricing source and owner identification.
- **CraftCalculationRequest (updated):** Integration with new profile and context models.

## Conclusion:
The specified updates have been successfully implemented in the `models.py` file, ensuring that all fields are properly normalized according to the requirements without breaking existing features. The code changes align precisely with the objective to support Phase 1 and Phase 1.5 functionalities for the Craft Calculator.