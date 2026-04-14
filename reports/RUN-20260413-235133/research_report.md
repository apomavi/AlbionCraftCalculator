## Source Inventory
- Pydantic documentation: https://pydantic.dev/docs/validation/latest/concepts/models/
- Stack Overflow question: https://stackoverflow.com/questions/71512035/how-should-i-specify-default-values-on-pydantic-fields-with-validate-always-to
- Medium article: https://medium.com/@marcnealer/a-practical-guide-to-using-pydantic-8aafa7feebf6

## Findings
Pydantic models can validate data in three different modes: Python, JSON, and strings. The Python mode gets used when using the `__init__()` model constructor. To handle default values like dictionaries, you should use a `Field` with a `default_factory`. This approach ensures that each instance of the model has its own separate dictionary.

## Constraints
- Pydantic models are mutable by default.
- Default values for fields can be specified using `Field` and `default_factory`.

## Implementation Notes
1. Use `Field` from `pydantic` to define fields with default values.
2. For dynamic default values like dictionaries, use `default_factory`.
3. Ensure that each instance of the model has its own separate dictionary by using `default_factory=dict`.

## Sources
- Pydantic documentation: https://pydantic.dev/docs/validation/latest/concepts/models/
- Stack Overflow question: https://stackoverflow.com/questions/71512035/how-should-i-specify-default-values-on-pydantic-fields-with-validate-always-to
- Medium article: https://medium.com/@marcnealer/a-practical-guide-to-using-pydantic-8aafa7feebf6