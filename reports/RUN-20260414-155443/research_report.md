## Source Inventory
The following file was analyzed: `src/albion_factory/craftcalc/models.py`.
The following web search was performed: "pydantic BaseModel default_factory dict example".

## Findings
The `src/albion_factory/craftcalc/models.py` file contains existing Pydantic models related to crafting calculations. The web search confirmed that `pydantic.Field(default_factory=dict)` is the correct way to handle default dictionary values for Pydantic model fields.

## Constraints
- Do not break existing fields.
- Use `pydantic.Field` where appropriate, especially for default values that require factory functions (e.g., `default_factory=dict`).

## Implementation Notes
The following changes will be made to `src/albion_factory/craftcalc/models.py`:

1.  **Create `PlayerProfile` model:**
    ```python
    class PlayerProfile(BaseModel):
        server: str = "europe"
        has_premium: bool = False
        global_crafting_discount: float = 0.0
        crafting_specs: dict[str, int] = Field(default_factory=dict)
        crafting_masteries: dict[str, int] = Field(default_factory=dict)
    ```
2.  **Create `LocationContext` model:**
    ```python
    class LocationContext(BaseModel):
        city: str
        is_black_zone: bool = False
        hideout_level: int = 0
        hideout_biome_bonus: bool = False
        is_headquarters: bool = False
    ```
3.  **Update `CraftPricePoint` model:**
    Add `source` and `owner_id` fields.
    ```python
    class CraftPricePoint(BaseModel):
        item_id: str
        city: str
        quality: int | None = None
        sell_price_min: float | None = None
        buy_price_max: float | None = None
        retrieved_at: str | None = None
        source: str = "AODP_PUBLIC"  # New field
        owner_id: str | None = None  # New field
    ```
4.  **Update `CraftCalculationRequest` model:**
    Add `player_profile` and `location_context` fields.
    ```python
    class CraftCalculationRequest(BaseModel):
        item_id: str
        city: str
        quality: int | None = None
        use_focus: bool = False
        include_taxes: bool = True
        player_profile: PlayerProfile | None = None  # New field
        location_context: LocationContext | None = None  # New field
    ```

## Sources
- `src/albion_factory/craftcalc/models.py`
- Pydantic Documentation on Fields: [https://pydantic-docs.helpdocs.io/latest/usage/fields/](https://pydantic-docs.helpdocs.io/latest/usage/fields/) (General reference for `Field` usage)