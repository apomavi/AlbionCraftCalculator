# Target Data

- `PlayerProfile` model (pydantic BaseModel):
  - `server` (str, default "europe")
  - `has_premium` (bool, default False)
  - `global_crafting_discount` (float, default 0.0)
  - `crafting_specs` (dict[str, int])
  - `crafting_masteries` (dict[str, int])

- `LocationContext` model (pydantic BaseModel):
  - `city` (str)
  - `is_black_zone` (bool, default False)
  - `hideout_level` (int, default 0)
  - `hideout_biome_bonus` (bool, default False)
  - `is_headquarters` (bool, default False)

- Update existing `CraftPricePoint` model:
  - Add `source` (str, default "AODP_PUBLIC")
  - Add `owner_id` (str | None, default None)

- Update existing `CraftCalculationRequest` model:
  - Add `player_profile` (PlayerProfile | None, default None)
  - Add `location_context` (LocationContext | None, default None)

# Collected Data

```json
{
  "PlayerProfile": {
    "server": "europe",
    "has_premium": false,
    "global_crafting_discount": 0.0,
    "crafting_specs": {},
    "crafting_masteries": {}
  },
  "LocationContext": {
    "city": "",
    "is_black_zone": false,
    "hideout_level": 0,
    "hideout_biome_bonus": false,
    "is_headquarters": false
  }
}
```

# Normalization Notes

- `PlayerProfile` and `LocationContext` models have been created with the specified fields.
- The `CraftPricePoint` model has been updated to include `source` and `owner_id`.
- The `CraftCalculationRequest` model has been updated to include `player_profile` and `location_context`.
- Default values are set as specified, and `pydantic.Field` is used where appropriate for default factories.