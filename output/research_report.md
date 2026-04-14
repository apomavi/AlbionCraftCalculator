# Research Report: Craft Calculator Phase 6 — Validation and Probe

## Source Inventory

*   **`scripts/probe_agents.py`**: This file is designated for the implementation of the validation, probe, and scoring logic. It currently serves as a target for development rather than containing pre-existing research findings on these specific topics.
*   **Provided Lead Plan**: This document outlines the project's scope, objectives, required agents, constraints (maintain request/run/report pipeline), and success criteria (defined validation criteria, established probe strategy, implemented scoring mechanism, full functional coverage).

## Findings

The objective is to continuously measure the accuracy of Craft Calculator outputs using agent probes and tests. This requires establishing a clear validation, probe, and scoring strategy within the existing `request/run/report` pipeline.

### 1. Validation Criteria

To ensure the accuracy and reliability of the Craft Calculator's outputs, the following validation criteria should be established:

*   **Known Item Fixtures:**
    *   **Definition:** A curated set of specific crafting recipes or item calculations with pre-determined, deterministic, and verified correct outputs.
    *   **Purpose:** To serve as ground truth for verifying the basic functional correctness of the calculator for common or critical scenarios.
    *   **Examples:** Expected cost of crafting a 'Basic Sword', profit margin for 'Advanced Potion', time taken for 'Masterwork Armor'.

*   **Expected Profitability Sanity Checks:**
    *   **Definition:** Rules based on domain knowledge to check if the calculated profitability of a craft falls within acceptable, logical bounds. This goes beyond mere calculation to encompass economic sense within the game/system.
    *   **Purpose:** To catch calculations that might be arithmetically correct but economically nonsensical or exploitable.
    *   **Examples:** A craft should not yield significantly negative profit if market prices are stable; profit margins should generally align with item rarity or complexity.

*   **Consistency and Determinism:**
    *   **Definition:** The calculator must produce identical outputs for identical inputs, regardless of when the calculation is performed (assuming no external data drift, like market prices, if applicable).
    *   **Purpose:** To ensure reliability and predictability of the core calculation engine.

*   **Range and Constraint Adherence:**
    *   **Definition:** Outputs must fall within predefined, logical ranges (e.g., crafting time > 0, resource costs are non-negative, derived values do not exceed system limits).
    *   **Purpose:** To validate that the calculator's outputs respect the physical or economic constraints of the system it models.

### 2. Probe Strategy

The strategy for probing agents will involve using domain-specific prompts to evaluate their understanding and the calculator's application in realistic scenarios.

*   **Domain-Specific Prompts:**
    *   **Definition:** Carefully crafted natural language queries that simulate user interactions or specific crafting scenarios within the game/system's context.
    *   **Purpose:** To test the agent's ability to interpret complex requests, leverage the Craft Calculator, and provide relevant, actionable answers.
    *   **Prompt Categories:**
        *   **Cost/Profit Analysis:** "What is the most profitable item to craft with [resource A, resource B]?"
        *   **Resource Optimization:** "If I have X units of item Y, how many Z can I craft?"
        *   **Comparative Analysis:** "Compare the crafting cost of Item P versus Item Q."
        *   **Scenario-Based:** "Estimate the profit if I craft 100 units of [item] during a market event where [condition]."

*   **Agent Response Evaluation:**
    *   **Accuracy:** Does the agent's answer correctly reflect the Craft Calculator's output?
    *   **Relevance:** Does the answer directly address the user's prompt?
    *   **Completeness:** Does the answer include all necessary information (e.g., costs, profits, resources, warnings)?
    *   **Interpretation:** Did the agent correctly understand quantities, units, and conditional modifiers in the prompt?

*   **Iterative and Comprehensive Probing:**
    *   Develop a diverse and expanding library of domain prompts.
    *   Regularly run probes to detect regressions or drift in agent performance.

### 3. Score Strategy

A scoring mechanism is essential for quantifying agent performance and identifying "weak agents."

*   **Metric Definition:** Scores should be derived from the success rate of validation criteria and probe tests.
    *   **Fixture Score:** Percentage of known item fixtures passing validation.
    *   **Profitability Sanity Check Score:** Percentage of profitability checks passing.
    *   **Domain Prompt Score:** A composite score reflecting accuracy, relevance, and completeness of responses to domain prompts. This might require a separate evaluation layer (human or oracle agent).
    *   **Consistency Score:** Measure of output stability across multiple runs of identical probes.

*   **Weak Agent Detection:**
    *   **Thresholds:** Define minimum acceptable score thresholds for each metric. Agents falling below these thresholds are flagged as weak.
    *   **Consolidated Score:** A weighted average of individual metric scores can provide an overall agent performance indicator.
    *   **Failure Analysis:** Log detailed reasons for score failures (e.g., "Incorrect profit calculation for recipe X," "Agent failed to interpret quantity '100+' in prompt Y").

*   **Pipeline Integration:** Probe results and calculated scores must be logged and reported within the existing `request/run/report` cycle, potentially as part of the final `report` or a dedicated performance summary.

## Constraints

*   **Request/Run/Report Pipeline Preservation:** All new validation, probing, and scoring functionalities must integrate seamlessly with the existing pipeline structure without disrupting its fundamental operation. The `probe` and `score` steps will logically follow `run` and precede or augment the `report`.
*   **Domain Specificity:** The validation criteria, probe prompts, and scoring logic must be tailored to the specific domain and mechanics of the target Craft Calculator.

## Implementation Notes

*   **`scripts/probe_agents.py` Role:** This file will be the central hub for implementing:
    *   **Data Management:** Loading and managing `known_item_fixtures` and `expected_profitability_checks` (e.g., from YAML or JSON files).
    *   **Validation Logic:** Functions to execute fixture checks, sanity checks, and consistency tests against calculator outputs.
    *   **Probe Execution:** Logic to construct and send domain-specific prompts to the agent and capture responses.
    *   **Response Evaluation:** Functions to score agent responses based on accuracy, relevance, and completeness.
    *   **Scoring Engine:** Logic to aggregate individual metric scores into overall agent performance and identify weak agents.
    *   **Reporting Integration:** Functions to log probe results and scores, feeding into the overall `manifest/report` system.

*   **Data Formats:**
    *   **Fixtures:** Use structured formats like YAML or JSON for `known_item_fixtures`. Each fixture should include input parameters, expected outputs, and potentially metadata like item ID or recipe name.
    *   **Prompts:** Store domain prompts in a categorized manner, perhaps with associated expected outcomes or evaluation criteria.

*   **Modularity and Extensibility:**
    *   Design the validation, probing, and scoring modules to be easily extendable. New item types, recipes, or validation rules should be straightforward to add.
    *   The scoring mechanism should allow for configurable weights for different metrics.

*   **Prompt Engineering Best Practices:**
    *   Develop a strategy for generating diverse prompts that cover edge cases, common scenarios, and complex interactions.
    *   Consider using prompt templates to ensure consistency and facilitate the generation of many related prompts.

*   **Feedback Loop:** Ensure that probe results and agent performance scores are clearly communicated and actionable for the development team responsible for improving the Craft Calculator and its associated agents.

## Sources

*   General principles of software testing and quality assurance.
*   Methodologies for validating machine learning models and AI agents, particularly in task-oriented domains.
*   Research and best practices in prompt engineering and agent evaluation frameworks.
*   The existing documentation and codebase structure related to the Craft Calculator's `request/run/report` pipeline.