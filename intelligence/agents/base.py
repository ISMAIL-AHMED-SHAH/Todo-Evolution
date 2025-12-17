"""
Base Agent Class

Foundation for all specialized agents in the intelligence layer.
"""

from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Base class for all agents."""

    def __init__(self, name: str, description: str):
        """
        Initialize base agent.

        Args:
            name: Agent name
            description: Agent description
        """
        self.name = name
        self.description = description
        self.history: List[Dict[str, Any]] = []

    @abstractmethod
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task.

        Args:
            task: Task specification

        Returns:
            Task result

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement execute()")

    def log_execution(self, task: Dict[str, Any], result: Dict[str, Any]) -> None:
        """
        Log task execution.

        Args:
            task: Task that was executed
            result: Execution result
        """
        self.history.append({
            "task": task,
            "result": result,
            "agent": self.name
        })

    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get execution history.

        Returns:
            List of execution records
        """
        return self.history

    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get agent capabilities.

        Returns:
            Dictionary describing agent capabilities
        """
        return {
            "name": self.name,
            "description": self.description,
            "skills": self._list_skills()
        }

    @abstractmethod
    def _list_skills(self) -> List[str]:
        """
        List available skills.

        Returns:
            List of skill names
        """
        raise NotImplementedError("Subclasses must implement _list_skills()")

    def __repr__(self) -> str:
        """String representation of agent."""
        return f"{self.__class__.__name__}(name='{self.name}')"
