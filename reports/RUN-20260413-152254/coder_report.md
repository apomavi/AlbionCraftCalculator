```
Target Files:
1. src/albion_factory/craftcalc/models

Planned Changes:
1. Add new model 'PlayerProfile' with the fields 'player_id' and 'nickname'.
2. Add new model 'LocationContext' with the fields 'context_name', 'coordinates', and 'region_id' (nullable).
3. Update 'CraftPricePoint' model to add an integer field 'minimum_level'. 
4. Update 'CraftCalculationRequest' model to change the 'is_active' field from BooleanField to a TextField.

Applied Changes:
1. Created new file `src/albion_factory/craftcalc/models/player_profile.py` with content:
```python
from django.db import models

class PlayerProfile(models.Model):
    player_id = models.CharField(max_length=255, primary_key=True)
    nickname = models.CharField(max_length=255, unique=True)
```
2. Created new file `src/albion_factory/craftcalc/models/location_context.py` with content:
```python
from django.db import models

class LocationContext(models.Model):
    context_name = models.CharField(max_length=255, primary_key=True)
    coordinates = models.JSONField()
    region_id = models.IntegerField(null=True)
```
3. Updated `src/albion_factory/craftcalc/models/craft_price_point.py` by adding the following line:
```python
minimum_level = models.IntegerField()
```
4. Updated `src/albion_factory/craftcalc/models/craft_calculation_request.py` by changing:
```python
is_active = models.BooleanField()
```
to
```python
is_active = models.TextField()
```

Remaining Risks:
1. Unit tests need to be updated or created for the new and modified models.
2. Database migrations are required and should be tested to ensure data integrity.
3. Integration testing is necessary to confirm that the changes do not impact other parts of the application.
4. Documentation should be updated to include new models and model fields.

write_repo_file: 
{
  "path": "src/albion_factory/craftcalc/models/player_profile.py",
  "content": "from django.db import models\nclass PlayerProfile(models.Model):\n    player_id = models.CharField(max_length=255, primary_key=True)\n    nickname = models.CharField(max_length=255, unique=True)"
}

write_repo_file: 
{
  "path": "src/albion_factory/craftcalc/models/location_context.py",
  "content": "from django.db import models\nclass LocationContext(models.Model):\n    context_name = models.CharField(max_length=255, primary_key=True)\n    coordinates = models.JSONField()\n    region_id = models.IntegerField(null=True)"
}

write_repo_file: 
{
  "path": "src/albion_factory/craftcalc/models/craft_price_point.py",
  "content": "from django.db import models\nclass CraftPricePoint(models.Model):\n    craftable_item = models.ForeignKey('CraftableItem', on_delete=models.CASCADE)\n    price_type = models.CharField(max_length=20, choices=[('buy', 'Buy'), ('sell', 'Sell')])\n    price_per_unit = models.DecimalField(max_digits=19, decimal_places=4)\n    minimum_level = models.IntegerField()"
}

write_repo_file: 
{
  "path": "src/albion_factory/craftcalc/models/craft_calculation_request.py",
  "content": "from django.db import models\nclass CraftCalculationRequest(models.Model):\n    requested_by_player = models.ForeignKey('PlayerProfile', on_delete=models.CASCADE)\n    requested_item = models.ForeignKey('CraftableItem', on_delete=models.CASCADE)\n    request_time = models.DateTimeField(auto_now_add=True)\n    is_active = models.TextField()"
}
```