### Target Data

1. **PlayerProfile Model**:
   - Fields:
     - `server`: str (default "europe")
     - `has_premium`: bool (default False)
     - `global_crafting_discount`: float (default 0.0)
     - `crafting_specs`: dict[str, int]
     - `crafting_masteries`: dict[str, int]

2. **LocationContext Model**:
   - Fields:
     - `city`: str
     - `is_black_zone`: bool (default False)
     - `hideout_level`: int (default 0)
     - `hideout_biome_bonus`: bool (default False)
     - `is_headquarters`: bool (default False)

3. **CraftPricePoint Model**:
   - Fields to Add:
     - `source`: str (default "AODP_PUBLIC")
     - `owner_id`: str | None (default None)

4. **CraftCalculationRequest Model**:
   - Fields to Add:
     - `player_profile`: PlayerProfile | None (default None)
     - `location_context`: LocationContext | None (default None)

### Collected Data

#### PlayerProfile
- **server**: 
  - Default: "europe"
  - Possible Values: "europe", "us", "asia", "australia" (based on Albion Online server locations)
- **has_premium**:
  - Default: False
  - Possible Values: True, False (indicating whether the player has premium status)
- **global_crafting_discount**:
  - Default: 0.0
  - Possible Values: Any float between 0.0 and 1.0 (e.g., 0.2 for a 20% discount)
- **crafting_specs**:
  - Keys: Crafting discipline names as strings (e.g., "Tailoring", "Cooking")
  - Values: Integer levels of specialization within each discipline
- **crafting_masteries**:
  - Keys: Crafting mastery names as strings (e.g., "Master Tailor", "Master Cook")
  - Values: Integer levels of mastery attained by the player

#### LocationContext
- **city**: 
  - Possible Values: Names of cities in Albion Online (e.g., "Caerleon", "Lymhurst", "Bridge", etc.)
- **is_black_zone**:
  - Default: False
  - Possible Values: True, False (indicating whether the location is a Black Zone)
- **hideout_level**:
  - Default: 0
  - Possible Values: Any integer from 1 to 5 (representing levels of hideouts in Albion Online)
- **hideout_biome_bonus**:
  - Default: False
  - Possible Values: True, False (indicating whether the hideout has biome bonuses)
- **is_headquarters**:
  - Default: False
  - Possible Values: True, False (indicating whether the location is a player headquarters)

### Normalization Notes

1. **Server Field**:
   - Standardized possible values to valid Albion Online server region names.
   - Ensured default value matches the predominant server.

2. **Crafting Specifications and Masteries**:
   - Defined keys as strings representing specific crafting disciplines and masteries within Albion Online.
   - Allowed integer values for levels, assuming a range from 1 upwards.

3. **Location Properties**:
   - Used string values for city names to maintain consistency with game data.
   - Boolean fields (`is_black_zone`, `hideout_biome_bonus`, `is_headquarters`) are standardized with appropriate default and possible value sets.

4. **Source and Owner ID in CraftPricePoint**:
   - Added `source` field with a default value of "AODP_PUBLIC".
   - Included `owner_id` as an optional string to capture crafting resource ownership or origins.

5. **PlayerProfile and LocationContext Links in CraftCalculationRequest**:
   - Added optional fields for linking player profile and location context directly to calculation requests, allowing for more granular and accurate calculations based on player status and environmental factors.

---

This data standardization ensures that the models are robust, flexible, and maintain consistency with Albion Online’s gameplay mechanics.