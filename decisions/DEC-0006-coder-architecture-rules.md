# DEC-0006 — Coder Architecture Rules

## Objective

Ensure coder outputs align with modern software architecture expectations.

## Coder Must

1. produce real implementation, not only summaries
2. prefer small, composable modules
3. separate domain models from service logic
4. separate calculation logic from IO/config logic
5. keep naming consistent and intention-revealing
6. add smoke-level verification when possible

## Required Design Tendencies

- domain models in dedicated modules
- service/resolver/engine logic in dedicated modules
- explicit data structures over implicit dictionaries where reasonable
- minimal side effects
- predictable interfaces

## Coder Must Avoid

- fake implementation reports without real file changes
- mixing unrelated concerns in one file
- speculative API contracts with no guardrails
- hiding uncertainty behind polished prose

## Preferred Pattern

- models.py -> data contracts
- *_resolver.py -> resolution logic
- *_engine.py -> calculation/comparison logic
- tests/test_*_smoke.py -> minimal verification

## Output Contract

Coder final output must include:
- Target Files
- Planned Changes
- Applied Changes
- Remaining Risks

## Validation Expectation

If coder did not create/update code where required, validator should not mark commit-ready.
