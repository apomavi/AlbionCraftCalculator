## Source Inventory
- Pydantic documentation on dicts and mapping types: [link](https://docs.pydantic.dev/2.3/usage/types/dicts_mapping/)
- Stack Overflow question on default values in Pydantic models: [link](https://stackoverflow.com/questions/76133124/do-not-assign-default-values-when-creating-model-from-dict-in-pydantic)
- GitHub discussion on assigning default value of a model to an empty dict: [link](https://github.com/pydantic/pydantic/discussions/8062)

## Findings
- Pydantic models do not support direct assignment of default values for dictionaries. Instead, you should use the `Field` class with `default_factory=dict`.
- The current implementation in `models.py` does not handle default dictionary values correctly.

## Constraints
- Directly assigning a dictionary as a default value will lead to unexpected behavior.
- Use `Field(default_factory=dict)` to ensure that each instance of the model has its own separate dictionary.

## Implementation Notes
- Review the `models.py` file and update any fields with dictionary types to use `Field(default_factory=dict)`.
- Ensure that all instances of the model are initialized correctly without shared mutable default values.

## Sources
- [Pydantic Docs on Dicts and Mapping Types](https://docs.pydantic.dev/2.3/usage/types/dicts_mapping/)
- [Stack Overflow: Do not assign default values when creating model from dict in Pydantic](https://stackoverflow.com/questions/76133124/do-not-assign-default-values-when-creating-model-from-dict-in-pydantic)
- [GitHub Discussion: How to assign default value of a model to an empty dict?](https://github.com/pydantic/pydantic/discussions/8062)