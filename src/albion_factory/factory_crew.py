from __future__ import annotations

from crewai import Agent, Task
from crewai.project import CrewBase, agent, task

from albion_factory.model_config import build_llm
from albion_factory.tools.factory_tools import (
    InspectRepoFileTool,
    NormalizeCsvNewlinesTool,
    ReadRepoFileTool,
    VerifyCsvStructureTool,
    VerifyTextStructureTool,
)


@CrewBase
class AlbionFactoryCrew:
    agents_config = "config/factory_agents.yaml"
    tasks_config = "config/factory_tasks.yaml"

    @agent
    def lead_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["lead_manager"],  # type: ignore[index]
            llm=build_llm("factory_lead_manager", self.agents_config["lead_manager"].get("llm")),  # type: ignore[index]
            verbose=True,
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],  # type: ignore[index]
            llm=build_llm("factory_researcher", self.agents_config["researcher"].get("llm"), enable_fallback=True),  # type: ignore[index]
            tools=[ReadRepoFileTool()],
            verbose=True,
        )

    @agent
    def coder(self) -> Agent:
        return Agent(
            config=self.agents_config["coder"],  # type: ignore[index]
            llm=build_llm("factory_coder", self.agents_config["coder"].get("llm")),  # type: ignore[index]
            tools=[InspectRepoFileTool(), NormalizeCsvNewlinesTool(), ReadRepoFileTool()],
            verbose=True,
        )

    @agent
    def tester(self) -> Agent:
        return Agent(
            config=self.agents_config["tester"],  # type: ignore[index]
            llm=build_llm("factory_tester", self.agents_config["tester"].get("llm")),  # type: ignore[index]
            tools=[VerifyCsvStructureTool(), VerifyTextStructureTool(), ReadRepoFileTool()],
            verbose=True,
        )

    @agent
    def validator(self) -> Agent:
        return Agent(
            config=self.agents_config["validator"],  # type: ignore[index]
            llm=build_llm("factory_validator", self.agents_config["validator"].get("llm")),  # type: ignore[index]
            tools=[VerifyCsvStructureTool(), VerifyTextStructureTool(), ReadRepoFileTool()],
            verbose=True,
        )

    @task
    def lead_task(self) -> Task:
        return Task(config=self.tasks_config["lead_task"])  # type: ignore[index]

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config["research_task"])  # type: ignore[index]

    @task
    def code_task(self) -> Task:
        return Task(config=self.tasks_config["code_task"])  # type: ignore[index]

    @task
    def test_task(self) -> Task:
        return Task(config=self.tasks_config["test_task"])  # type: ignore[index]

    @task
    def validation_task(self) -> Task:
        return Task(config=self.tasks_config["validation_task"])  # type: ignore[index]