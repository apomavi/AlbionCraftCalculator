The file `src/albion_factory/craftcalc/models.py` needs to be updated to include the `PlayerProfile` and `LocationContext` Pydantic models, and to ensure the `CraftPricePoint` and `CraftCalculationRequest` models have the specified fields.

**Existing `CraftPricePoint` Model Analysis:**
The file `src/albion_factory/craftcalc/models.py` currently defines `CraftPricePoint` with the following relevant fields:
- `owner_id: str | None = None`
- `source: str = "AODP_PUBLIC"`
These fields are already present in the existing code, although `owner_id` is marked with a comment "Note: added owner_id and source from legacy AODP_PUBLIC". The implementation should ensure these fields are correctly defined and utilized as per the requirement.

**Existing `CraftCalculationRequest` Model Analysis:**
The file `src/albion_factory/craftcalc/models.py` currently defines `CraftCalculationRequest` with placeholders for the new models:
- `player_profile: PlayerProfile | None = None # type: ignore`
- `location_context: LocationContext | None = None # type: ignore`
These indicate that the `PlayerProfile` and `LocationContext` models are expected to be defined and then referenced here.

**New Models to be Created:**
The following Pydantic models need to be created within `src/albon_factory/craftcalc/models.py`:

1.  **`PlayerProfile` model:**
    ```python
    from pydantic import BaseModel, Field

    class PlayerProfile(BaseModel):
        server: str = "europe"
        has_premium: bool = False
        global_crafting_discount: float = 0.0
        crafting_specs: dict[str, int] = Field(default_factory=dict)
        crafting_masteries: dict[str, int] = Field(default_factory=dict)
    ```

2.  **`LocationContext` model:**
    ```python
    from pydantic import BaseModel, Field

    class LocationContext(BaseModel):
        city: str
        is_black_zone: bool = False
        hideout_level: int = 0
        hideout_biome_bonus: bool = False
        is_headquarters: bool = False
    ```

**Updates to Existing Models:**
-   **`CraftPricePoint`:** Ensure `source` (str, default "AODP_PUBLIC") and `owner_id` (str | None, default None) are correctly defined. Based on the file content, these fields are already present.
-   **`CraftCalculationRequest`:** Ensure `player_profile` (PlayerProfile | None, default None) and `location_context` (LocationContext | None, default None) are correctly defined, referencing the newly created models. The placeholders with `# type: ignore` should be updated to reflect the actual type hints after `PlayerProfile` and `LocationContext` are defined.

This forms the basis for the Coder to implement the required changes in `src/albion_factory/craftcalc/models.py`.