The `models.py` file in the repository defines several Pydantic models for handling craft recipes and related data in an application. The key models include:

- **CraftRecipeIngredient**: Represents an ingredient in a crafting recipe, with fields for item ID, item name, and quantity.
- **CraftRecipe**: Represents a complete crafting recipe, including the output item details and a list of ingredients.
- **CraftPricePoint**: Captures price information for items in different cities, with optional quality specifications and timestamps.
- **CraftRuleSet**: Contains rules specific to a city, such as crafting fees, sales taxes, usage fees, resource return rates, and focus enablement status.
- **CraftCalculationRequest**: Represents a request for calculating the profitability of crafting an item, including details like item ID, city, quality, and whether focus should be used.
- **CraftCalculationResult**: Stores the results of a profitability calculation, including estimated input cost, output value, profit, margin, break-even price, and any notes.