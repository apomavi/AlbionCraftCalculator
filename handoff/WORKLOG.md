# WORKLOG

## 2026-04-13 — Initial Handoff System Created

### What was established
- Created persistent cross-AI handoff structure
- Added live project context file
- Added reusable master prompt for other AI systems
- Added session template for future takeover runs

### Existing project state at handoff creation time
- Canonical production workflow exists
- Feedback-aware routing exists in `src/albion_factory/production_flow.py`
- Validator feedback fields exist in config/contracts
- Raw tool dump detection exists
- Validator output normalization exists

### Known remaining issues at this point
- Agent output quality is improved but still not perfect
- Quality tuning is now mostly behavioral, not architectural
- Probe/scoring logic may still be improved further

### Key files to monitor
- `src/albion_factory/production_flow.py`
- `src/albion_factory/config/agents.yaml`
- `src/albion_factory/config/tasks.yaml`
- `scripts/probe_agents.py`
- `scripts/score_agent_probe.py`

## 2026-04-14 — Data Collector Integration & Strict Prompts

### What changed
- `data_collector` added to canonical CrewAI production flow (`crew.py`, `production_flow.py`, `agents.yaml`, `tasks.yaml`).
- Upgraded `_extract_field` logic in validator parsing to support multi-line text blocks reliably (re.DOTALL support).
- Added very strict anti-JSON rules to `tester` and `validator` in `agents.yaml` and `tasks.yaml`.
- Updated handoff and context files to reflect the 6-agent standard.

## 2026-04-14 — Quality and Probe System Fixes

### What changed
- Added `data_collector` to `probe_agents.py` and `score_agent_probe.py` so it can be evaluated.
- Stricter source citation rules added to `researcher` prompt in `agents.yaml` to fix the "WEAK" score detected in previous probe runs.

## 2026-04-14 — General Automation Factory Decoupling

### What changed
- Removed hardcoded Craft Calculator locks (`REQ-0005..REQ-0010` and `target_file` mappings) from `scripts/run_request_phase.py`.
- The production flow now relies entirely on the Lead and Coder agents to determine target files and scope.
- The system is now a fully generic arbitrary job executor.

## 2026-04-14 — Phase 1 & 1.5 Architecture Models Built

### What changed
- Added `PlayerProfile` and `LocationContext` models to `src/albion_factory/craftcalc/models.py`.
- Added `source` and `owner_id` fields to `CraftPricePoint` to support future Private Client ingestion, defaulting to `AODP_PUBLIC`.
- Updated `CraftCalculationRequest` to include profile and location contexts.

## 2026-04-14 — Feedback Loop Enhancements & Logging Visibility

### What changed
- Increased `MAX_RETRIES_PER_AGENT` from 2 to 5 in `src/albion_factory/production_flow.py` for better automatic recovery.
- Exported all intermediate agent outputs (`lead`, `researcher`, `coder`, `tester`, `validator`) into the final result dictionary.
- Updated `scripts/run_request_phase.py` to write these agent states as separate Markdown and JSON files in the `reports/RUN-...` directory.

## 2026-04-14 — Feedback Loop Flow Routing Fix & Strict Tool Usage

### What changed
- Fixed a routing break in `production_flow.py`. Retries now properly use `or_` logic to route cycles back into the main pipeline correctly, instead of silently dropping into untracked listener methods.
- Enforced strict `write_repo_file` tool usage in `agents.yaml` and `tasks.yaml` to prevent the Coder agent from just outputting markdown code blocks without persisting them.
- Tightened Tester prompt to prevent JSON command leaks into final outputs.

## 2026-04-14 — Revert Manual Models for AI Execution

### What changed
- Reverted the manual addition of `PlayerProfile` and `LocationContext` from `models.py`.
- This was done to allow the CrewAI Coder agent to perform the actual implementation for REQ-0011 as a test of the newly fixed feedback loop and strict tool usage rules.

## 2026-04-14 — Fake Pass Vulnerability Fix & LLM Upgrade

### What changed
- Fixed a logical vulnerability in `production_flow.py` where a `Verdict: PASS` would bypass the feedback loop even if `Commit Ready: NO` was returned. Now, both conditions must be strictly met.
- Switched `coder` and `tester` LLMs from local `ollama/qwen2.5-coder:14b` to `gemini/gemini-2.5-flash` in `agents.yaml` to permanently resolve persistent formatting issues where agents leaked raw JSON tool dumps instead of valid markdown.

## 2026-04-14 — Feedback Loop FSM State Routing Overhaul

### What changed
- Completely removed the buggy `or_` operator logic from `production_flow.py`.
- Replaced the linear graph with an explicit Finite State Machine (FSM) by placing `@router` checkpoints after every agent step. This guarantees that retries will accurately re-enter the workflow without premature exits.

## 2026-04-14 — Global LLM Fallback Activation

### What changed
- Activated `enable_fallback=True` for all agents in `crew.py` (Lead, Data Collector, Coder, Tester, Validator). Previously, only the Researcher had this enabled.
- Upgraded default models for Lead and Validator to `gemini-2.5-flash` in `agents.yaml` to ensure stronger reasoning, keeping `flash-lite` only for simple data collection/research.
- Added `503`, `unavailable`, and `overloaded` triggers to `_is_quota_like_error` in `model_config.py` to prevent flow crashes during Gemini API spikes.
- Implemented role-specific fallback chains in `model_config.py`. Heavy technical roles (coder/tester) prioritize `qwen2.5-coder:14b` on fallback, while reasoning roles prioritize `flash`, and research prioritizes `flash-lite`.

## 2026-04-14 — Local LLM Hallucination Guardrails & Validator Self-Correction

### What changed
- Strengthened `_contains_embedded_tool_dump` in `production_flow.py` to catch non-standard local LLM tool-call hallucinations (e.g., Qwen's `write_repo_file: { ... }` format).
- Added a self-correction loop for the `validator` agent in `production_flow.py`. If the validator fails to output the required Markdown headers, it will now be routed back to itself for correction instead of instantly failing the entire flow.

## 2026-04-14 — Context Hallucination Guardrails

### What changed
- Added strict anti-hallucination rules to `agents.yaml` and `tasks.yaml` to prevent the Coder from mistaking code snippets in the Data Collector's report for the actual state of the files.
- Forced the Coder to always use `read_repo_file` before deciding if changes are needed.
- Forced the Tester to never trust the Coder's claims without verifying the actual file content.

## 2026-04-14 — Local LLM Stability & Anti-Hallucination Measures

### What changed
- Set `temperature=0.0` for all LLM instantiations in `model_config.py` to prevent local models (like `qwen2.5-coder:14b`) from hallucinating unrequested fields or Django ORM syntax in a Pydantic project.
- Injected a `STRICT INSTRUCTION` at the very end of `_build_prompt_for_agent` in `production_flow.py` to exploit LLM recency bias and force strict markdown header adherence.
- Translated the "output contract" instructions in `agents.yaml` to English to improve instruction-following for smaller local models.

## 2026-04-14 — ReAct Pattern Restoration & Validator Loop Fix

### What changed
- Modified the `STRICT INSTRUCTION` in `production_flow.py` to explicitly allow tool usage *before* the Final Answer. Previously, the strict markdown constraint overrode the local model's ReAct syntax, causing it to skip tool calls entirely and hallucinate actions.
- Fixed the Validator infinite self-correction loop in `production_flow.py`. Instead of checking for the presence of an error string (which the LLM could echo back), the parser now uses a deterministic `validator_format_failed` boolean flag.

## 2026-04-14 — ReAct Loop Escape & Temperature Tuning

### What changed
- Added an explicit JSON dictionary requirement for `Action Input` in `production_flow.py`'s `STRICT INSTRUCTION` prompt to prevent local models from omitting `{}`.
- Changed LLM instantiations in `model_config.py` from `temperature=0.0` to `temperature=0.1` to introduce just enough entropy for local models to break out of deterministic ReAct error loops without sacrificing general instruction adherence.

## 2026-04-14 — Strict Validator Parsing & Syntax Fix

### What changed
- Fixed a syntax error (missing `or`) in `_contains_embedded_tool_dump` which could break the pipeline evaluating tester outputs.
- Updated `_normalize_validator_output` to check that *all* 7 required headers are present. If any are missing, the `validator_format_failed` flag triggers the self-correction loop, preventing silent drops to a `none` target when the LLM hallucinates partial headers.

## 2026-04-14 — Fill-in-the-Blanks Template Pattern & Hallucination Override

### What changed
- Replaced the loose "adhere to this contract" instructions in `agents.yaml` with explicit literal templates (e.g. `## Scope\n[text]`). This "Fill-in-the-Blanks" pattern is highly effective at preventing smaller local models from outputting JSON or skipping headers.
- Replaced the Coder's read directive in `tasks.yaml` and `agents.yaml` with an aggressive override, explicitly telling the Coder that the code provided by the Data Collector is *not* currently in the file and *must* be written using `write_repo_file`. This stops the Coder from falsely claiming the file is already up to date.

## 2026-04-14 — Safe Agent Kickoff Wrapper

### What changed
- Added a `_safe_kickoff` wrapper function in `production_flow.py` to wrap `agent.kickoff()` calls in a `try-except` block.
- Prevented the entire CrewAI Flow and Python process from crashing if a local LLM agent hits the `max_iterations` limit and returns a `ValueError` or empty response.
- Instead of a hard crash, the failed agent now outputs an `AGENT CRASHED` string that naturally flows downstream to the Validator, which will route it back to the failing agent for a retry.

## 2026-04-14 — Anti-Array Tool Call Enforcement

### What changed
- Updated the `STRICT INSTRUCTION` block in `production_flow.py` to explicitly demonstrate the exact ReAct tool call format (`Thought` / `Action` / `Action Input`).
- Added a critical rule explicitly forbidding the use of JSON arrays/lists `[...]` for Action Inputs, forcing local models (like `qwen2.5-coder:14b`) to use standard dictionaries `{...}` instead.
- This resolves the infinite loop parsing error caused when the local LLM tries to pass a list of arguments to LangChain/CrewAI tools.

## 2026-04-14 — ReAct Prompt Simplification & Validator Relaxation

### What changed
- Removed the overly verbose `Thought/Action` template from `production_flow.py`'s `STRICT INSTRUCTION`. This was overwhelming the local model and causing it to skip tool calls entirely.
- Removed the strict `all()` check for Validator headers in `production_flow.py`. If the Validator misses a minor header, it no longer triggers an infinite self-correction loop, allowing the flow to proceed gracefully.
- Added an absolute directive to the Coder in `tasks.yaml` forbidding it from generating a Final Answer without actually executing `write_repo_file`.

## 2026-04-14 — Anti-Chatter / JSON Parsing Fix

### What changed
- Added an aggressive "STOP WRITING" directive to `production_flow.py`'s `STRICT INSTRUCTION`.
- This prevents the local LLM (Qwen) from appending extraneous arrays or comments immediately after a valid tool-call JSON dictionary, which was previously breaking the LangChain parser and causing infinite ReAct loops.

## 2026-04-14 — Positive Reinforcement Prompting Fix

### What changed
- Refactored the tool-call constraint in `production_flow.py` to use purely positive reinforcement.
- Removed the explicit negative constraint "Never use an array `[...]`", which ironically caused the local LLM to hallucinate and append array characters (Ironic Process Theory / Pink Elephant Paradox).
- Replaced it with a strict positive constraint: "MUST be exactly one JSON object starting with `{` and ending with `}`".

## 2026-04-14 — LLM Stop Sequences Applied

### What changed
- Added explicit `stop` sequences (`["Observation:", "[No observation", "\n["]`) to all `LLM` instantiations in `model_config.py`.
- This hard-cuts the LLM generation immediately after it finishes outputting JSON for a tool call.
- Prevents the local Qwen model from hallucinating "Observation" sections or extra arrays, which were triggering CrewAI/LangChain's aggressive auto-json-repair to incorrectly nest the payload into an array.
- Added a rule to `production_flow.py` strictly forbidding the use of empty lists `[]` inside Action Input parameters to prevent triggering JSON parser list combinations.

## 2026-04-14 — ReAct Prompt Simplification & Validator Relaxation

### What changed
- Removed the strict `all()` check for Validator headers in `production_flow.py`. If the Validator misses a minor header, it no longer triggers an infinite self-correction loop, allowing the flow to proceed gracefully.
- Added the explicit `Action` / `Action Input` template back to the `STRICT INSTRUCTION` prompt to prevent the Coder from trying to format tools incorrectly, now that array hallucinations are physically blocked by stop words.

## 2026-04-14 — Qwen-Tamer Auto-Saver Interceptor

### What changed
- Removed `WriteRepoFileTool` from the `coder` agent in `crew.py` to stop forcing local models to write multiline code via strict JSON payloads, which was causing severe hallucinations and tool skips.
- Re-tasked the `coder` in `agents.yaml` and `tasks.yaml` to instead output raw code within a ````python` block under `## Applied Changes`.
- Added an Auto-Saver Interceptor directly in `production_flow.py`'s `coder` listener. This intercepts the LLM output, extracts the target file and code block, and writes it directly to the local disk, bypassing the need for agent tool execution entirely.

## 2026-04-14 — Root Cause Fix: Tool Restored & Context Poisoning Prevented

### What changed
- Removed the "Auto-Saver" hack from `production_flow.py` as it caused agent blindness and false assumptions.
- Restored `WriteRepoFileTool` to the `coder` agent in `crew.py` so it physically implements files again.
- Simplified the `production_flow.py` strict instructions to remove conflicting `Action Input` formats that were breaking the CrewAI tool parser.
- Added aggressive guardrails to `agents.yaml` forbidding the `data_collector` from outputting Python classes, which was poisoning the context window and making the `coder` falsely believe files were already updated.
- Restored explicit `read_repo_file` directives to the `coder` in `tasks.yaml`.

## 2026-04-14 — English Constraints & ReAct Format Enforcement

### What changed
- Translated critical agent constraints in `agents.yaml` and `tasks.yaml` to English. LLMs (especially Flash Lite and Qwen) were ignoring the strict Turkish instructions (e.g., forbidding Python code output in Data Collector), leading to context poisoning.
- Restored the exact, unformatted text template for `Action:` and `Action Input:` in `production_flow.py`'s `STRICT INSTRUCTION`. 
- This stops Qwen from hallucinating markdown JSON blocks (`{"action": "read_file"}`) which LangChain's ReAct parser could not interpret, effectively restoring the Coder and Tester's ability to use tools correctly.

## 2026-04-14 — Tester Tool Blindness Fix

### What changed
- Updated `RunSafeCommandTool` description in `ops_tools.py` to explicitly forbid `echo`, `cat`, and shell pipelines, listing only the allowed prefixes.
- Added a critical rule to `agents.yaml` for the tester, forbidding the creation of temporary files via `echo` and forcing the use of `read_repo_file`. This breaks the 48-iteration infinite loop where the agent tried to execute an unallowed command.

## 2026-04-14 — LLM Context Window Expansion Fix

### What changed
- Added `num_ctx=16384` to all `LLM` initializations in `model_config.py`.
- Ollama defaults to a 2048 token context length, which caused local models like `qwen2.5-coder:14b` to silently forget tools, system prompts, and constraints once the context window was filled by large repository files.
- This fixes the root cause of the "blind stubbornness" where agents would enter infinite repetition loops trying to use disallowed tools, simply because their rules were evicted from the top of the context window.

## 2026-04-14 — Provider-Specific Context Length & Debug Cleanup

### What changed
- Removed `num_ctx=16384` completely from `model_config.py`.
- CrewAI utilizes LiteLLM's OpenAI compatibility layer to communicate with Ollama for better tool support. The underlying OpenAI Python client strictly rejects the `num_ctx` argument, resulting in an immediate hard crash (`unexpected keyword argument 'num_ctx'`). 
- Context expansion must be handled at the Ollama server level (`OLLAMA_NUM_CTX` environment variable) rather than passed via LLM kwargs in this architecture.
- Removed the raw LLM output debugger from `model_config.py` as it is no longer needed.

## 2026-04-14 — Conditional Tool Instructions

### What changed
- Updated `_build_prompt_for_agent` in `production_flow.py` to only append explicit `Action / Action Input` tool formatting instructions for agents that actually possess tools (`researcher`, `coder`, `tester`).
- This prevents tool-less agents (like `data_collector`, `lead`, and `validator`) from becoming confused by the tool template and hallucinating invalid actions (e.g., `Action: data_collector`), which previously resulted in infinite iteration loops.

## 2026-04-14 — Agent Role Evolution (Data Collector & Tester)

### What changed
- **Data Collector** upgraded: Granted `FetchUrlTool`, `FetchUrlToFileTool`, and `SmartResearchTool`. Prompt updated to focus on fetching external/API data and building raw datasets rather than just summarizing. Added to tool-usage instruction group in `production_flow.py`.
- **Tester** upgraded: Transformed into an aggressive QA engineer. Prompt updated to mandate running actual tests (e.g., `pytest` via `run_safe_command`), hunting for edge cases, and exposing logical bugs like zero-division errors, rather than just verifying file text structure.
- **Researcher** updated: Re-focused entirely on domain logic, math formulas, and architectural constraints, handing off all raw data fetching to the Data Collector.

## 2026-04-14 — Data Collector Local File Hallucination Fix

### What changed
- Updated `data_collector` backstory in `agents.yaml` and `tasks.yaml` to explicitly forbid using `fetch_url` for local repository files, directing it to use `read_repo_file` or skip fetching entirely if no external data is needed.
- Fixed an edge case where local fallback models (Qwen) would enter an infinite ReAct loop trying to fetch placeholder GitHub URLs (`your-repo/your-branch`) when forced to act as a data collector for pure code-refactoring tasks.

### Rule for future updates
After any important change, append a dated entry here with:
- what changed
- why it changed
- what was validated
- what remains open
