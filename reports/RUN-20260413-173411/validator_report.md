## Verdict
FAIL

## Evidence Used
- The content of `models.py` was read, but no specific details about the implementation were provided.
- No evidence of testing results or validation checks were included.

## Risks
- The absence of detailed implementation and testing evidence increases the risk of undetected issues in the code.
- There is a high likelihood that critical functionality may not have been thoroughly tested.

## Required Fixes
- Provide the actual content of the updated `models.py` file to verify the implementation details.
- Include comprehensive test results to ensure that all changes work as expected and do not break existing functionality.
- Ensure that all required fields are correctly implemented and that default values are set appropriately using `pydantic.Field`.

## Feedback Target
researcher

## Feedback Reason
The researcher agent crashed or returned an empty response, which led to the failure of this run. The Validator must mark this run as FAIL and set Feedback Target to 'researcher' so it can retry.

## Commit Ready
NO
