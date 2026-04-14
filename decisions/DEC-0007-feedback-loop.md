# DEC-0007 — Agent Feedback Loop

## Objective

If tester or validator finds a negative result, feedback must return to the responsible agent before finalization.

## Principle

Negative findings should not just be reported.
They should trigger a targeted correction loop.

## Feedback Fields

Validator should produce:
- Verdict
- Evidence Used
- Risks
- Required Fixes
- Feedback Target
- Feedback Reason
- Commit Ready

## Allowed Feedback Targets

- `researcher`
- `coder`
- `tester`
- `none`

## Routing Logic

- PASS + Commit Ready YES -> finalize success
- PARTIAL/FAIL + Feedback Target researcher -> return to researcher
- PARTIAL/FAIL + Feedback Target coder -> return to coder
- PARTIAL/FAIL + Feedback Target tester -> return to tester
- PARTIAL/FAIL + Feedback Target none -> finalize failure

## Retry Policy

- retry should be agent-specific, not global-only
- repeated failure should preserve evidence and feedback history
