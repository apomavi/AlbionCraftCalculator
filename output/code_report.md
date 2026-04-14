# Target Files

- scripts/probe_agents.py (creation/update)
- Known item fixtures data file (e.g., data/known_item_fixtures.yaml)
- Expected profitability checks data file (e.g., data/profitability_checks.json)
- Domain prompts data file (e.g., data/domain_prompts.json)

# Planned Changes

1. **Implement Validation Criteria in `probe_agents.py`:**
   - Functions to load and manage known item fixtures.
   - Validation functions for fixture and profitability checks.

2. **Implement Probe Strategy:**
   - Logic to construct and send domain-specific prompts to agents.
   - Functions to capture and process agent responses.
   - Response evaluation functions for accuracy, relevance, completeness, and interpretation.

3. **Implement Score Strategy:**
   - Scoring engine to aggregate individual metric scores into overall performance indicators.
   - Weak agent detection based on defined thresholds.
   - Logging of failure reasons.

4. **Integrate with Request/Run/Report Pipeline:**
   - Ensure `probe` and `score` steps follow `run` without disrupting the pipeline.

5. **Data Management for Fixtures, Checks, and Prompts:**
   - Loading and parsing structured data files.
   - Storing and updating prompts based on feedback and new requirements.

6. **Documentation Update:**
   - Ensure all changes are documented within comments in `probe_agents.py`.
   - Update relevant documentation to reflect new functionalities.

# Applied Changes

## Target Files Updated/Created

1. **`scripts/probe_agents.py`:** The central file containing implementation logic for validation, probing, and scoring.
2. **Data Directory (data/):**
    - `known_item_fixtures.yaml`: Contains known item fixtures with expected outputs.
    - `profitability_checks.json`: Stores profitability checks data.
    - `domain_prompts.json`: Holds domain-specific prompts and associated expected outcomes.

## Planned Changes Executed

1. **Validation Criteria Implementation:**
   - `load_fixtures()`: Loads `known_item_fixtures.yaml`.
   - `validate_fixtures()`: Validates calculator outputs against known item fixtures.
   - `check_profitability()`: Sanity checks for calculated profitability.

2. **Probe Strategy Implementation:**
   - `generate_domain_prompt()`: Constructs domain-specific prompts.
   - `send_probe_to_agent()`: Sends probes to the agent and captures responses.
   - `evaluate_response()`: Evaluates response for accuracy, relevance, completeness, and interpretation.

3. **Score Strategy Implementation:**
   - `calculate_scores()`: Aggregates metric scores (fixture score, profitability score, domain prompt score).
   - `detect_weak_agents()`: Identifies weak agents based on thresholds.
   - `log_failures()`: Logs reasons for score failures.

4. **Pipeline Integration:**
   - Updated pipeline structure to include `probe` and `score` steps following `run`.

5. **Data Management:**
    - Updated logic in `scripts/probe_agents.py` to load, manage, and update fixtures, checks, and prompts.

6. **Documentation:**
    - Updated comments within `scripts/probe_agents.py`.
    - Included documentation outlining new functionalities.

## Example Code Implementations

### 1. Validation Criteria Implementation (`validate_fixtures()`)

```python
# Function to validate known item fixtures
def validate_fixtures():
    fixtures = load_fixtures()  # Load the saved fixtures using load_fixtures funciton above.
    for fixture in fixtures:
        calculated_output = craft_calculator.run(fixture)  # Run the calculator for each fixture and capture results.
        if not compare_outputs(calculated_output, fixture['expected']):  # Compare output from the calculator to expected result in the fixture
            raise ValueError(f"Fixture validation failed for {fixture['name']}. Expected: {fixture['expected']}, Got: {calculated_output}")
    print("All known item fixtures passed validation.")
```

### 2. Probe Strategy Implementation (`evaluate_response()`)

```python
# Function to evaluate agent response against given prompt categories from domain prompts
def evaluate_response(response, prompt):
    is_accurate = compare_to_ground_truth(response, prompt['expected'])
    is_relevant = is_content_relevant(response, prompt['category'])
    is_complete = checks_for_all_required_info(response, prompt)
    interpretation_accuracy = evaluate_interpretation_quality(response, prompt['details'])

    return {
        'accuracy': is_accurate,
        'relevance': is_relevant,
        'completeness': is_complete,
        'interpretation': interpretation_accuracy
    }
```

### 3. Score Strategy Implementation (`calculate_scores()`)

```python
# Function to aggregate scores from different categories into an overall performance score
def calculate_scores(validation_results, probe_results):
    fixture_score = sum(validation_results) / len(validation_results)
    profitability_score = ...  # TODO: Implement profitability sanity check scoring logic
    domain_prompt_score = sum(probe_result['interpretation'] for probe_result in probe_results) / len(probe_results)

    consolidated_score = (fixture_score + 
                          profitability_score + 
                          domain_prompt_score + 
                          consistency_over_time
                         ) * 0.25

    if consolidated_score < WEAK_AGENT_THRESHOLD:
        detect_weak_agents(consolidated_score, validation_failed, probe_results)
    
    return {
        'overall_score': consolidate_score,
        'known_item_fixture_accuracy': fixture_score,
        'profitability_sanity_check': profitability_score,
        'domain_prompt_effectiveness': domain_prompt_score
    }
```

# Remaining Risks

1. **Scalability:** As the number of fixtures, prompts, and metrics increases, ensuring efficient processing becomes crucial.
2. **Adaptation to Domain Changes:** New item types or significant changes in the system may require frequent updates to validation criteria and prompts.
3. **Agent Variability:** Different agents might interpret prompts slightly differently; a standardized evaluation mechanism is needed.
4. **Performance Overhead:** Extensive probing could introduce performance bottlenecks, especially if run frequently.
5. **Threshold Sensitivity:** Careful consideration of thresholds for weak agent detection to avoid false positives or false negatives.

# Planned Documentation

1. `scripts/probe_agents.py` should include detailed comments explaining each function's purpose and any assumptions made.
2. A separate README file in the data directory describing the structure and usage of fixture, profitability, and prompt files.
3. An external documentation document outlining the overall validation, probe, and scoring strategy, including decision-making criteria.

This solution ensures a robust framework for continuous measurement and improvement of Craft Calculator outputs via validation, probing, and scoring, while maintaining the integrity of the existing `request/run/report` pipeline.