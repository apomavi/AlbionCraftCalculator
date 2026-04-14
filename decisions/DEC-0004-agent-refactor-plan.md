# DEC-0004 — Agent Refactor Implementation Plan

## Objective

Replace the current fragmented CrewAI topology with a single primary production workflow aligned to the following roles:

- lead
- researcher
- coder
- tester
- validator

## Refactor Phases

### Phase 1 — Topology Simplification

#### Goal
Reduce role duplication and clarify ownership.

#### Actions
1. Decide which crew is the canonical production workflow.
2. Deprecate or demote duplicated crews.
3. Separate optional helper roles from the main pipeline.

#### Expected Result
- one primary implementation path
- no ambiguous request routing

---

### Phase 2 — Role Redefinition

#### Goal
Make each agent's responsibility explicit.

#### Actions
1. Rewrite lead as process owner/orchestrator.
2. Rewrite coder as full implementation owner.
3. Tighten tester and validator contracts.
4. Simplify researcher role split.

#### Expected Result
- clear inputs
- clear outputs
- no duplicated responsibilities

---

### Phase 3 — LLM Realignment

#### Goal
Assign models by role responsibility.

#### Proposed Direction
- lead → reliable planning model
- researcher → search/reasoning fallback chain
- coder → primary local coding model
- tester → stable deterministic model
- validator → conservative review model

#### Expected Result
- model selection is role-driven, not historical/accidental

---

### Phase 4 — Generic Coder Tooling

#### Goal
Enable real non-CSV implementation work.

#### Actions
1. Add generic create/update/patch tool.
2. Attach that tool to coder.
3. Remove dependence on CSV-only implementation behavior.

#### Expected Result
- coder can write real code
- request phases can produce implementation, not just summaries

---

### Phase 5 — Workflow Rewire

#### Goal
Route request phases through the corrected production path.

#### Actions
1. Rework request routing.
2. Align phase requests with the canonical workflow.
3. Re-run from `REQ-0005` sequentially.

#### Expected Result
- request → run → report works with the corrected topology

---

### Phase 6 — Validation

#### Goal
Verify that the new topology behaves as intended.

#### Actions
1. compile / smoke test
2. request phase replay
3. probe/scoring after refactor

#### Expected Result
- no orphan roles
- no fake coder behavior
- validator becomes a real gate

## Immediate Next Action

Start with Phase 1 and Phase 2 together:
- choose the canonical production crew
- rewrite agent definitions around that topology