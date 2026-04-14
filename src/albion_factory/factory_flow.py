from __future__ import annotations

from pathlib import Path
from typing import TypedDict

from crewai.flow.flow import Flow, listen, router, start

from albion_factory.factory_crew import AlbionFactoryCrew


class FactoryState(TypedDict, total=False):
    factory_request: str
    target_file: str
    lead_output: str
    research_output: str
    coder_output: str
    tester_output: str
    validator_output: str
    retry_count: int
    verdict: str


class AlbionFactoryFlow(Flow[FactoryState]):
    MAX_RETRIES = 1

    def _is_csv_target(self) -> bool:
        return self.state.get("target_file", "").lower().endswith(".csv")

    def _required_terms_for_target(self) -> list[str]:
        target = self.state.get("target_file", "")
        if target.endswith("models.py"):
            return ["class CraftRecipe", "class CraftPricePoint", "class CraftCalculationRequest"]
        return []

    @start()
    def request_intake(self):
        if "factory_request" not in self.state:
            self.state["factory_request"] = "Fix newline formatting in data/logs/import_runs.csv"
        if "target_file" not in self.state:
            self.state["target_file"] = "data/logs/import_runs.csv"
        if "retry_count" not in self.state:
            self.state["retry_count"] = 0
        return self.state

    @listen(request_intake)
    def lead_manager(self, _state):
        crew = AlbionFactoryCrew()
        result = crew.lead_manager().kickoff(
            f"Request: {self.state['factory_request']}\nTarget File: {self.state['target_file']}"
        )
        self.state["lead_output"] = result.raw
        return result.raw

    @listen(lead_manager)
    def researcher(self, _lead_output):
        crew = AlbionFactoryCrew()
        result = crew.researcher().kickoff(
            f"Request: {self.state['factory_request']}\n"
            f"Target File: {self.state['target_file']}\n"
            "Read the target file, explain the current issue, root cause, and minimal fix."
        )
        self.state["research_output"] = result.raw
        return result.raw

    @listen(researcher)
    def coder(self, _research_output):
        crew = AlbionFactoryCrew()
        if self._is_csv_target():
            instruction = (
                "First inspect the target file. Then use the normalize_csv_newlines tool on the target file. "
                "Return output with these headings: Target Files, Planned Changes, Applied Changes, Remaining Risks."
            )
        else:
            instruction = (
                "Inspect the target file and produce an implementation-oriented summary only. "
                "Do not apply CSV-specific tools to non-CSV files. "
                "Return output with these headings: Target Files, Planned Changes, Applied Changes, Remaining Risks."
            )
        result = crew.coder().kickoff(
            f"Request: {self.state['factory_request']}\n"
            f"Target File: {self.state['target_file']}\n"
            f"{instruction}"
        )
        self.state["coder_output"] = result.raw
        return result.raw

    @listen(coder)
    def tester(self, _coder_output):
        crew = AlbionFactoryCrew()
        if self._is_csv_target():
            instruction = "Use verify_csv_structure and return output with these headings: Test Steps, Findings, Evidence, Verdict."
        else:
            required_terms = self._required_terms_for_target()
            instruction = (
                "Use verify_text_structure for the target file and return output with these headings: "
                f"Test Steps, Findings, Evidence, Verdict. Required terms: {required_terms}"
            )
        result = crew.tester().kickoff(
            f"Target File: {self.state['target_file']}\n"
            f"Coder Output:\n{self.state['coder_output']}\n"
            f"{instruction}"
        )
        self.state["tester_output"] = result.raw
        return result.raw

    @listen(tester)
    def validator(self, _tester_output):
        crew = AlbionFactoryCrew()
        result = crew.validator().kickoff(
            f"Request: {self.state['factory_request']}\n"
            f"Target File: {self.state['target_file']}\n"
            f"Coder Output:\n{self.state['coder_output']}\n"
            f"Tester Output:\n{self.state['tester_output']}\n"
            "Return output with these headings: Verdict, Reason, Commit Ready, Required Fixes. "
            "Only say Commit Ready: YES if tester evidence is sufficient and target-specific structure is valid."
        )
        self.state["validator_output"] = result.raw
        verdict = "FAIL"
        if "PASS" in result.raw.upper() and "COMMIT READY: YES" in result.raw.upper():
            verdict = "PASS"
        self.state["verdict"] = verdict
        return result.raw

    @router(validator)
    def route_validation(self, _validator_output):
        if self.state.get("verdict") == "PASS":
            return "pass"

        retry_count = self.state.get("retry_count", 0)
        if retry_count < self.MAX_RETRIES:
            self.state["retry_count"] = retry_count + 1
            return "retry"
        return "fail"

    @listen("retry")
    def retry_coder(self, _label):
        return self.coder(self.state.get("research_output", ""))

    @listen("pass")
    def pass_result(self, _label):
        return {
            "status": "PASS",
            "target_file": self.state["target_file"],
            "retry_count": self.state.get("retry_count", 0),
            "validator_output": self.state["validator_output"],
        }

    @listen("fail")
    def fail_result(self, _label):
        return {
            "status": "FAIL",
            "target_file": self.state["target_file"],
            "retry_count": self.state.get("retry_count", 0),
            "validator_output": self.state["validator_output"],
        }


def kickoff(factory_request: str | None = None, target_file: str | None = None):
    flow = AlbionFactoryFlow()
    if factory_request:
        flow.state["factory_request"] = factory_request
    if target_file:
        flow.state["target_file"] = target_file
    return flow.kickoff()