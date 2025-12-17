"""
Agent Runner

Executes individual agents and manages their lifecycle.
"""

from typing import Dict, Any, List, Optional
import logging

from ..agents.base import BaseAgent


logger = logging.getLogger(__name__)


class AgentRunner:
    """Runner for executing individual agents."""

    def __init__(self):
        """Initialize agent runner."""
        self.execution_log: List[Dict[str, Any]] = []

    def run(
        self,
        agent: BaseAgent,
        task: Dict[str, Any],
        verbose: bool = False
    ) -> Dict[str, Any]:
        """
        Run an agent with a task.

        Args:
            agent: Agent to execute
            task: Task specification
            verbose: Enable verbose logging

        Returns:
            Execution result

        Example:
            >>> from intelligence.agents import RAGKnowledgeAgent
            >>> runner = AgentRunner()
            >>> agent = RAGKnowledgeAgent()
            >>> result = runner.run(agent, {
            ...     "skill": "retrieve_docs",
            ...     "params": {"library": "fastapi"}
            ... })
        """
        if verbose:
            logger.info(f"Running {agent.name} with task: {task}")

        try:
            result = agent.execute(task)

            self.execution_log.append({
                "agent": agent.name,
                "task": task,
                "result": result,
                "status": "success"
            })

            if verbose:
                logger.info(f"Task completed successfully: {result}")

            return result

        except Exception as e:
            error_result = {
                "error": str(e),
                "agent": agent.name,
                "task": task
            }

            self.execution_log.append({
                "agent": agent.name,
                "task": task,
                "result": error_result,
                "status": "error"
            })

            if verbose:
                logger.error(f"Task failed: {e}")

            return error_result

    def run_batch(
        self,
        agent: BaseAgent,
        tasks: List[Dict[str, Any]],
        verbose: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Run an agent with multiple tasks.

        Args:
            agent: Agent to execute
            tasks: List of task specifications
            verbose: Enable verbose logging

        Returns:
            List of execution results

        Example:
            >>> runner = AgentRunner()
            >>> agent = RAGKnowledgeAgent()
            >>> results = runner.run_batch(agent, [
            ...     {"skill": "retrieve_docs", "params": {"library": "fastapi"}},
            ...     {"skill": "summarize_spec", "params": {"feature_name": "auth"}}
            ... ])
        """
        results = []

        for i, task in enumerate(tasks):
            if verbose:
                logger.info(f"Running task {i+1}/{len(tasks)}")

            result = self.run(agent, task, verbose=verbose)
            results.append(result)

        return results

    def get_execution_log(self) -> List[Dict[str, Any]]:
        """
        Get execution log.

        Returns:
            List of execution records
        """
        return self.execution_log

    def clear_log(self) -> None:
        """Clear execution log."""
        self.execution_log = []

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get execution statistics.

        Returns:
            Statistics dictionary
        """
        total = len(self.execution_log)
        successful = sum(1 for log in self.execution_log if log["status"] == "success")
        failed = total - successful

        agents_used = {}
        for log in self.execution_log:
            agent_name = log["agent"]
            agents_used[agent_name] = agents_used.get(agent_name, 0) + 1

        return {
            "total_executions": total,
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / total * 100) if total > 0 else 0,
            "agents_used": agents_used
        }
