# DEC-0003 — Agent Topology Audit

## Status

Draft — requires implementation follow-up.

## Problem

Current CrewAI topology in this repository has grown organically and now mixes:
- report-oriented agents
- implementation-oriented agents
- operations-oriented agents

This creates role overlap, weak ownership, and unclear process boundaries.

## Current Problems

### 1. Report crew vs Factory crew split is too fragmented

Current split:
- `report crew`: lead / researcher / validator
- `factory crew`: lead_manager / researcher / coder / tester / validator
- `ops crew`: lead_manager / researcher / data_collector / tester / validator

Problem:
- same concepts are repeated across multiple crews
- responsibilities drift between crews
- request routing becomes ambiguous
- user intent is production/implementation-heavy, not separate report pipelines

### 2. Lead role is under-specified or mispositioned

Lead should be:
- process owner
- task distributor
- scope controller
- acceptance criteria owner
- handoff manager between agents

Lead should NOT mainly behave like:
- mini analyst
- generic reporter
- duplicate researcher

### 3. Coder role is not yet a real coder

Current blocker:
- coder has no generic create/update/patch capability for non-CSV files
- therefore coder often produces plans or summaries instead of real implementation

Required correction:
- coder must become the primary implementation agent
- coder must own real file creation/update/patch actions

### 4. Research roles are over-split

Current state:
- report researcher
- factory researcher
- ops researcher

Problem:
- too much duplication
- weak ownership boundaries
- prompts drift apart

Preferred direction:
- either one core researcher
- or at most two:
  - domain/web researcher
  - repo/code researcher

### 5. Tester and validator need stricter gate behavior

Tester should:
- produce commands
- produce evidence
- summarize findings
- give verdict

Validator should:
- produce PASS / PARTIAL / FAIL
- produce commit-ready decision
- explain evidence used
- list required fixes

### 6. LLM assignment should follow role responsibility, not file history

Preferred direction:
- Lead → most reliable planner model
- Researcher → search/reasoning fallback chain
- Coder → primary local coding model (`qwen2.5-coder:14b`) once generic patch tool exists
- Tester → deterministic and stable model
- Validator → conservative and consistent model

## Proposed Correct Topology

### Single Primary Production Crew

Recommended core team:
- `lead`
- `researcher`
- `coder`
- `tester`
- `validator`

Optional helper roles:
- `data_collector` only when explicit external/file collection is needed

### Role Definitions

#### Lead
- reads request
- understands project/phase scope
- breaks work into steps
- selects required agents
- defines inputs/outputs for each agent
- controls scope and quality gates

#### Researcher
- gathers repo context
- gathers domain/web evidence
- identifies missing data and risks
- produces implementation-ready research notes

#### Coder
- writes actual code
- creates/updates files
- applies patches
- reports what changed

#### Tester
- runs compile/tests/smoke checks
- produces evidence
- explains findings

#### Validator
- final quality gate
- PASS/PARTIAL/FAIL
- commit-ready decision
- required fixes

## Required Technical Corrections

1. add generic file create/update/patch tool for coder
2. stop using CSV-specific implementation flow as the default factory path
3. reduce or refactor duplicated crews
4. make request routing deterministic
5. align all agent contracts to the corrected topology

## Immediate Next Refactor

1. define a single canonical production workflow
2. implement generic coder tool layer
3. rewire request phases to that workflow
4. re-run craft calculator requests from `REQ-0005`