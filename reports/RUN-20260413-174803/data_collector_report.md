## Target Data
- `PlayerProfile` model with fields: `server`, `has_premium`, `global_crafting_discount`, `crafting_specs`, `crafting_masteries`
- `LocationContext` model with fields: `city`, `is_black_zone`, `hideout_level`, `hideout_biome_bonus`, `is_headquarters`
- Update `CraftPricePoint` model to include `source` and `owner_id`
- Update `CraftCalculationRequest` model to include `player_profile` and `location_context`

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
  },
  "CraftPricePoint": {
    "source": "AODP_PUBLIC",
    "owner_id": null
  },
  "CraftCalculationRequest": {
    "player_profile": null,
    "location_context": null
  }
}
```

## Normalization Notes
- Used `pydantic.Field(default_factory=dict)` for dictionary fields to ensure each instance has its own separate dictionary.
- Ensured that all instances of the model are initialized correctly without shared mutable default values.