from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool


@CrewBase
class AlbionFactory:
    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def lead(self) -> Agent:
        return Agent(
            config=self.agents_config["lead"],
            verbose=True,
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            verbose=True,
            tools=[SerperDevTool()],
        )

    @agent
    def validator(self) -> Agent:
        return Agent(
            config=self.agents_config["validator"],
            verbose=True,
            tools=[SerperDevTool()],
        )

    @task
    def planning_task(self) -> Task:
        return Task(
            config=self.tasks_config["planning_task"]
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"]
        )

    @task
    def validation_task(self) -> Task:
        return Task(
            config=self.tasks_config["validation_task"]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )