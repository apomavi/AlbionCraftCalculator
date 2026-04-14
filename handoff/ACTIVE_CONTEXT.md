# ACTIVE_CONTEXT

## Purpose

This file is the live project memory for any AI taking over work in this repository.
It must be updated after major architectural, workflow, or implementation changes.

## Project Summary

- Repository name: `albion_factory`
- Current orchestration model: CrewAI-based production workflow
- Current canonical role set:
  - lead
  - researcher
  - data_collector
  - coder
  - tester
  - validator

## Canonical Architecture

### Decision Files
- `decisions/DEC-0003-agent-topology-audit.md`
- `decisions/DEC-0004-agent-refactor-plan.md`
- `decisions/DEC-0005-agent-operating-model.md`
- `decisions/DEC-0006-coder-architecture-rules.md`
- `decisions/DEC-0007-feedback-loop.md`

### Core Runtime Files
- `src/albion_factory/config/agents.yaml`
- `src/albion_factory/config/tasks.yaml`
- `src/albion_factory/crew.py`
- `src/albion_factory/production_flow.py`
- `scripts/run_request_phase.py`
- `scripts/probe_agents.py`
- `scripts/score_agent_probe.py`

## Current Workflow

1. Lead reads request
2. Researcher gathers repo/domain/web context
3. Data Collector gathers raw external/local data needed
4. Coder performs real implementation
5. Tester produces commands/evidence/findings/verdict
6. Validator gives final structured decision
6. If negative result exists, feedback is routed to the responsible agent
7. Retry is agent-specific
8. Finalization occurs only after pass or retry exhaustion

## Feedback-Aware Loop Status

Implemented in:
- `src/albion_factory/production_flow.py`

Current state fields:
- `feedback_target`
- `feedback_reason`
- `retry_counts`
- `feedback_history`

Current behavior:
- validator output is parsed for feedback fields
- routing can return to `researcher`, `data_collector`, `coder`, or `tester`
- raw tool-call dumps are treated as quality failures
- validator output is normalized into a strict section format

## Current Quality Risks

Remaining issues are mostly behavior-tuning issues, not architecture gaps:

1. Some agents may still produce weak or overly generic outputs
2. Tester may still produce low-quality command/evidence sections even if no raw JSON is present
3. Validator may technically conform after normalization, but still be semantically weak
4. Probe prompts may need continued tuning for stronger discipline

## Craft Calculator Module Status

Existing module skeletons:
- `src/albion_factory/craftcalc/models.py`
- `src/albion_factory/craftcalc/recipe_resolver.py`
- `src/albion_factory/craftcalc/price_resolver.py`
- `src/albion_factory/craftcalc/profit_engine.py`
- `src/albion_factory/craftcalc/comparison_engine.py`

Smoke coverage exists in:
- `tests/test_recipe_resolver_smoke.py`
- `tests/test_price_resolver_smoke.py`
- `tests/test_profit_engine_smoke.py`
- `tests/test_comparison_engine_smoke.py`
- `tests/test_probe_agents_smoke.py`
- `tests/test_score_agent_probe_smoke.py`

## Important Operational Notes

- Ollama local service must be running for `ollama/qwen2.5-coder:14b`
- `.env` currently sets `MODEL_DEFAULT=ollama/qwen2.5-coder:14b`
- Gemini is configured via `GEMINI_API_KEY`
- Provider strings should always include the provider prefix

## Current Best Next Actions

1. Continue hardening agent output quality
2. Improve scoring penalties for low-quality structured outputs
3. Keep handoff files updated after every major implementation
4. Use this file plus `MASTER_PROMPT.md` for cross-AI continuation
