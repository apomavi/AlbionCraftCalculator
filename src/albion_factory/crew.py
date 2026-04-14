from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from albion_factory.model_config import build_llm
from albion_factory.tools.factory_tools import ReadRepoFileTool, VerifyTextStructureTool, WriteRepoFileTool
from albion_factory.tools.ops_tools import RunSafeCommandTool, FetchUrlTool, FetchUrlToFileTool
from albion_factory.tools.research_tools import GeminiWebSearchProbeTool, SmartResearchTool


@CrewBase
class AlbionFactory:
    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def lead(self) -> Agent:
        return Agent(
            config=self.agents_config["lead"],  # type: ignore[index]
            llm=build_llm("report_lead", self.agents_config["lead"].get("llm"), enable_fallback=True),  # type: ignore[index]
            verbose=True,
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],  # type: ignore[index]
            llm=build_llm("report_researcher", self.agents_config["researcher"].get("llm"), enable_fallback=True),  # type: ignore[index]
            verbose=True,
            tools=[ReadRepoFileTool(), GeminiWebSearchProbeTool(), SmartResearchTool()],
        )

    @agent
    def data_collector(self) -> Agent:
        return Agent(
            config=self.agents_config["data_collector"],  # type: ignore[index]
            llm=build_llm("factory_data_collector", self.agents_config["data_collector"].get("llm"), enable_fallback=True),  # type: ignore[index]
            verbose=True,
            tools=[SmartResearchTool(), FetchUrlTool(), FetchUrlToFileTool(), ReadRepoFileTool()],
        )

    @agent
    def coder(self) -> Agent:
        return Agent(
            config=self.agents_config["coder"],  # type: ignore[index]
            llm=build_llm("factory_coder", self.agents_config["coder"].get("llm"), enable_fallback=True),  # type: ignore[index]
            verbose=True,
            tools=[ReadRepoFileTool(), WriteRepoFileTool()],
        )

    @agent
    def tester(self) -> Agent:
        return Agent(
            config=self.agents_config["tester"],  # type: ignore[index]
            llm=build_llm("factory_tester", self.agents_config["tester"].get("llm"), enable_fallback=True),  # type: ignore[index]
            verbose=True,
            tools=[VerifyTextStructureTool(), RunSafeCommandTool(), ReadRepoFileTool()],
        )

    @agent
    def validator(self) -> Agent:
        return Agent(
            config=self.agents_config["validator"],  # type: ignore[index]
            llm=build_llm("factory_validator", self.agents_config["validator"].get("llm"), enable_fallback=True),  # type: ignore[index]
            verbose=True,
        )

    @task
    def planning_task(self) -> Task:
        return Task(
            config=self.tasks_config["planning_task"]  # type: ignore[index]
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],  # type: ignore[index]
            context=[self.planning_task()],
        )

    @task
    def data_collection_task(self) -> Task:
        return Task(
            config=self.tasks_config["data_collection_task"],  # type: ignore[index]
            context=[self.research_task()],
        )

    @task
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config["code_task"],  # type: ignore[index]
            context=[self.data_collection_task(), self.research_task()],
        )

    @task
    def test_task(self) -> Task:
        return Task(
            config=self.tasks_config["test_task"],  # type: ignore[index]
            context=[self.code_task()],
        )

    @task
    def validation_task(self) -> Task:
        return Task(
            config=self.tasks_config["validation_task"],  # type: ignore[index]
            context=[self.test_task()],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )