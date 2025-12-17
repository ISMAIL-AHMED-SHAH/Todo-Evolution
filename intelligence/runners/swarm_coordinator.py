"""
Swarm Coordinator

Coordinates multiple agents working together on complex tasks.
"""

from typing import Dict, Any, List, Optional
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..agents.base import BaseAgent
from .agent_runner import AgentRunner


logger = logging.getLogger(__name__)


class SwarmCoordinator:
    """Coordinator for managing multiple agents in a swarm."""

    def __init__(self, max_workers: int = 4):
        """
        Initialize swarm coordinator.

        Args:
            max_workers: Maximum number of concurrent agent executions
        """
        self.max_workers = max_workers
        self.agent_runner = AgentRunner()
        self.agents: Dict[str, BaseAgent] = {}

    def register_agent(self, agent: BaseAgent) -> None:
        """
        Register an agent with the swarm.

        Args:
            agent: Agent to register

        Example:
            >>> from intelligence.agents import RAGKnowledgeAgent, BackendImplementationAgent
            >>> coordinator = SwarmCoordinator()
            >>> coordinator.register_agent(RAGKnowledgeAgent())
            >>> coordinator.register_agent(BackendImplementationAgent())
        """
        self.agents[agent.name] = agent
        logger.info(f"Registered agent: {agent.name}")

    def run_sequential(
        self,
        workflow: List[Dict[str, Any]],
        verbose: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Run a sequential workflow of agent tasks.

        Args:
            workflow: List of task specifications with agent names
            verbose: Enable verbose logging

        Returns:
            List of execution results

        Example:
            >>> coordinator = SwarmCoordinator()
            >>> results = coordinator.run_sequential([
            ...     {"agent": "RAG-Knowledge-Agent", "skill": "retrieve_docs", "params": {...}},
            ...     {"agent": "Backend-Implementation-Agent", "skill": "generate_models_sqlmodel", "params": {...}}
            ... ])
        """
        results = []

        for i, task_spec in enumerate(workflow):
            agent_name = task_spec.get("agent")
            task = {
                "skill": task_spec.get("skill"),
                "params": task_spec.get("params", {})
            }

            if agent_name not in self.agents:
                results.append({
                    "error": f"Agent not found: {agent_name}",
                    "task": task_spec
                })
                continue

            agent = self.agents[agent_name]

            if verbose:
                logger.info(f"Step {i+1}/{len(workflow)}: {agent_name}")

            result = self.agent_runner.run(agent, task, verbose=verbose)
            results.append(result)

        return results

    def run_parallel(
        self,
        tasks: List[Dict[str, Any]],
        verbose: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Run tasks in parallel across multiple agents.

        Args:
            tasks: List of task specifications with agent names
            verbose: Enable verbose logging

        Returns:
            List of execution results

        Example:
            >>> coordinator = SwarmCoordinator()
            >>> results = coordinator.run_parallel([
            ...     {"agent": "RAG-Knowledge-Agent", "skill": "retrieve_docs", ...},
            ...     {"agent": "Frontend-Implementation-Agent", "skill": "auth_ui_components", ...}
            ... ])
        """
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_task = {}

            for task_spec in tasks:
                agent_name = task_spec.get("agent")
                task = {
                    "skill": task_spec.get("skill"),
                    "params": task_spec.get("params", {})
                }

                if agent_name not in self.agents:
                    results.append({
                        "error": f"Agent not found: {agent_name}",
                        "task": task_spec
                    })
                    continue

                agent = self.agents[agent_name]
                future = executor.submit(self.agent_runner.run, agent, task, verbose)
                future_to_task[future] = task_spec

            for future in as_completed(future_to_task):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    task_spec = future_to_task[future]
                    results.append({
                        "error": str(e),
                        "task": task_spec
                    })

        return results

    def run_pipeline(
        self,
        pipeline: List[Dict[str, Any]],
        verbose: bool = False
    ) -> Dict[str, Any]:
        """
        Run a data processing pipeline where each step's output feeds the next.

        Args:
            pipeline: List of pipeline stage specifications
            verbose: Enable verbose logging

        Returns:
            Final pipeline result

        Example:
            >>> coordinator = SwarmCoordinator()
            >>> result = coordinator.run_pipeline([
            ...     {"agent": "RAG-Knowledge-Agent", "skill": "get_database_schema"},
            ...     {"agent": "Backend-Implementation-Agent", "skill": "generate_models_sqlmodel",
            ...      "params_from_previous": ["entities"]}
            ... ])
        """
        context = {}

        for i, stage in enumerate(pipeline):
            agent_name = stage.get("agent")
            skill = stage.get("skill")
            params = stage.get("params", {})

            # Extract params from previous stage results
            params_from_previous = stage.get("params_from_previous", [])
            for param_name in params_from_previous:
                if param_name in context:
                    params[param_name] = context[param_name]

            task = {"skill": skill, "params": params}

            if agent_name not in self.agents:
                return {
                    "error": f"Agent not found: {agent_name}",
                    "stage": i,
                    "context": context
                }

            agent = self.agents[agent_name]

            if verbose:
                logger.info(f"Pipeline stage {i+1}/{len(pipeline)}: {agent_name}.{skill}")

            result = self.agent_runner.run(agent, task, verbose=verbose)

            # Update context with result
            if isinstance(result, dict):
                context.update(result)

        return context

    def list_agents(self) -> List[Dict[str, str]]:
        """
        List registered agents.

        Returns:
            List of agent information
        """
        return [
            {
                "name": agent.name,
                "description": agent.description,
                "skills": agent._list_skills()
            }
            for agent in self.agents.values()
        ]

    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """
        Get an agent by name.

        Args:
            name: Agent name

        Returns:
            Agent or None if not found
        """
        return self.agents.get(name)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get execution statistics.

        Returns:
            Statistics dictionary
        """
        return self.agent_runner.get_statistics()
