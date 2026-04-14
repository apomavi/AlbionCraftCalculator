# DEC-0005 — General Agent Operating Model

## Objective

Define a reusable operating model so agents are not locked to a single product/domain.

## Core Principle

Agents must be **general-purpose workers with stable roles**, not one-off prompt fragments tied to a single feature.

## Canonical Workflow

1. **Lead** reads request
2. **Lead** defines scope, required agents, constraints, success criteria, next step
3. **Researcher** gathers repo/domain/web context
4. **Coder** performs real implementation
5. **Tester** produces command/evidence/findings/verdict
6. **Validator** gives final PASS/PARTIAL/FAIL + commit-ready

## Role Contracts

### Lead
- owns process
- assigns work
- defines handoffs
- controls scope
- never becomes the main implementer

### Researcher
- produces implementation-ready context
- identifies risks and missing information
- avoids speculative claims

### Coder
- writes code
- creates/updates files
- applies patches
- explains applied changes

### Tester
- runs technical checks
- produces evidence
- summarizes outcomes

### Validator
- acts as final quality gate
- requires evidence
- decides commit readiness

## Handoff Rules

- Lead -> Researcher: context and questions
- Researcher -> Coder: implementation notes and constraints
- Coder -> Tester: changed files and expected behavior
- Tester -> Validator: evidence and verdict

## Output Discipline

- agents may use tools
- final output must be human-readable markdown
- final output must never end as raw tool-call JSON

## Failure Handling

- if research is insufficient -> validator returns PARTIAL/FAIL
- if implementation is missing -> validator returns FAIL
- if evidence is insufficient -> validator returns FAIL

## Reuse Rule

This operating model should work for:
- Albion craft calculator
- repo maintenance
- data workflows
- validation and implementation tasks
