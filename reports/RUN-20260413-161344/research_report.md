The `models.py` file in the repository defines several Pydantic models related to crafting calculations in an Albion Online factory context. These models include:

- **CraftRecipeIngredient**: Represents an ingredient required for a craft recipe, including the item ID, name, and quantity.
- **CraftRecipe**: Represents a craft recipe, including the recipe ID, output item details, and a list of ingredients.
- **CraftPricePoint**: Represents price information for an item in a specific city, including sell and buy prices, quality, and retrieval time.
- **CraftRuleSet**: Represents rules applicable to crafting in a specific city, such as fees, taxes, resource return rates, and focus usage.
- **CraftCalculationRequest**: Represents a request for calculating the profitability of crafting an item, including the item ID, city, quality, focus usage, and tax inclusion.
- **CraftCalculationResult**: Represents the result of a crafting calculation, including estimated costs, values, profit margins, and notes.