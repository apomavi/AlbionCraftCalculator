from __future__ import annotations

from crewai import Agent, Task
from crewai.project import CrewBase, agent, task

from albion_factory.model_config import build_llm
from albion_factory.tools.ops_tools import (
    FetchUrlToFileTool,
    FetchUrlTool,
    ReadRepoFileTool,
    RunSafeCommandTool,
    SearchRepoFilesTool,
)
from albion_factory.tools.research_tools import GeminiWebSearchProbeTool, SmartResearchTool


@CrewBase
class AlbionOpsCrew:
    agents_config = "config/ops_agents.yaml"
    tasks_config = "config/ops_tasks.yaml"

    @agent
    def lead_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["lead_manager"],  # type: ignore[index]
            llm=build_llm("ops_lead_manager", self.agents_config["lead_manager"].get("llm")),  # type: ignore[index]
            verbose=True,
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],  # type: ignore[index]
            llm=build_llm("ops_researcher", self.agents_config["researcher"].get("llm"), enable_fallback=True),  # type: ignore[index]
            tools=[
                ReadRepoFileTool(),
                SearchRepoFilesTool(),
                FetchUrlTool(),
                GeminiWebSearchProbeTool(),
                SmartResearchTool(),
            ],
            verbose=True,
        )

    @agent
    def data_collector(self) -> Agent:
        return Agent(
            config=self.agents_config["data_collector"],  # type: ignore[index]
            llm=build_llm("ops_data_collector", self.agents_config["data_collector"].get("llm")),  # type: ignore[index]
            tools=[FetchUrlToFileTool(), ReadRepoFileTool()],
            verbose=True,
        )

    @agent
    def tester(self) -> Agent:
        return Agent(
            config=self.agents_config["tester"],  # type: ignore[index]
            llm=build_llm("ops_tester", self.agents_config["tester"].get("llm")),  # type: ignore[index]
            tools=[RunSafeCommandTool(), ReadRepoFileTool()],
            verbose=True,
        )

    @agent
    def validator(self) -> Agent:
        return Agent(
            config=self.agents_config["validator"],  # type: ignore[index]
            llm=build_llm("ops_validator", self.agents_config["validator"].get("llm")),  # type: ignore[index]
            tools=[ReadRepoFileTool(), FetchUrlTool()],
            verbose=True,
        )

    @task
    def lead_task(self) -> Task:
        return Task(config=self.tasks_config["lead_task"])  # type: ignore[index]

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config["research_task"])  # type: ignore[index]

    @task
    def data_task(self) -> Task:
        return Task(config=self.tasks_config["data_task"])  # type: ignore[index]

    @task
    def test_task(self) -> Task:
        return Task(config=self.tasks_config["test_task"])  # type: ignore[index]

    @task
    def validation_task(self) -> Task:
        return Task(config=self.tasks_config["validation_task"])  # type: ignore[index]