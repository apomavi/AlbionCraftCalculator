## Target Data

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

## Collected Data

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

## Normalization Notes

- The `PlayerProfile` model includes default values for all fields as specified.
- The `LocationContext` model also includes default values for all fields, with the `city` field being a required string.
- The `CraftPricePoint` and `CraftCalculationRequest` models have been updated to include the new fields with appropriate default values.