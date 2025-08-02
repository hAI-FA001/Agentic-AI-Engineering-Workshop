from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class Team():
    """Team crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode='safe',  # Docker
            max_execution_time=120,
            max_retry_limit=3,
        )

    @task
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_task']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Team crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
