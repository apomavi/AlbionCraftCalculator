## Lead Plan for Craft Calculator Phase 6 — Validation and Probe

### Scope
- **Objective:** Develop and implement a validation/probe/score strategy to ensure the accuracy of craft calculator outputs.
- **Activities:**
  - Define validation criteria for the outputs of the craft calculator.
  - Establish a probe strategy to continuously monitor and validate these outputs.
  - Create a scoring mechanism to evaluate agent performance and detect weak agents.
  - Ensure that the request/run/report/probe/score pipeline is maintained throughout the development process.

### Required Agents
- **Researcher:** Conduct research to establish best practices in validation and probe strategies for machine learning models. Provide insights on domain-specific prompts.
- **Coder:** Implement the defined validation criteria, probe strategy, and scoring mechanism in `scripts/probe_agents.py`.
- **Tester:** Perform functional testing against known item fixtures, expected profitability sanity checks, and agent responses to ensure accuracy and reliability of the validation framework.
- **Validator:** Validate the output results from the probes to ensure they adhere to the established criteria and provide feedback for further refinement.

### Constraints
- **Maintain the request/run/report pipeline structure.** Ensure that all new functionalities fit within this existing workflow without disrupting it.

### Success Criteria
- **Validation Criteria Defined:** Clear validation rules for all aspects of craft calculator outputs are outlined.
- **Probe Strategy Established:** A robust probe strategy is in place to continuously monitor and validate the calculator’s outputs.
- **Scoring Mechanism Implemented:** A functional scoring system that can detect weak agents based on their performance is operational.
- **Functional Coverage Achieved:** All key components, including known item fixtures, expected profitability checks, domain prompts, score-based agent detection, and manifest/report generation are fully tested and working as intended.

### Next Task
- Review the initial implementation by the coder to ensure it meets the defined criteria and constraints.
- Test the new framework thoroughly with the tester, focusing on edge cases and potential failure points.
- Validate the results using real-world scenarios and refine the strategies based on feedback from the validator.
- Ensure that all changes are documented and integrated into the main codebase.

## Next steps
```json
{
  "Task": "Review and integrate updated validation/probe/scoring mechanisms",
  "Assigned Agents": ["Coder", "Tester", "Validator"],
  "Deadline": "Within 1 week"
}
```

This plan ensures that the craft calculator outputs are consistently validated, probed, and evaluated to maintain high standards of accuracy and performance. Each step in the process is carefully defined, ensuring both success criteria and constraints are met.