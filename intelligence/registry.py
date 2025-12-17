"""
Agent Registry

Central registration and access point for all agents.
"""

from typing import Dict, Any, List, Optional
from .agents import (
    RAGKnowledgeAgent,
    BackendImplementationAgent,
    FrontendImplementationAgent,
    AuthIntegrationAgent,
    DatabaseSchemaAgent,
    BaseAgent
)


class AgentRegistry:
    """Central registry for all agents."""

    def __init__(self):
        """Initialize agent registry."""
        self._agents: Dict[str, BaseAgent] = {}
        self._register_default_agents()

    def _register_default_agents(self) -> None:
        """Register default agents."""
        default_agents = [
            RAGKnowledgeAgent(),
            BackendImplementationAgent(),
            FrontendImplementationAgent(),
            AuthIntegrationAgent(),
            DatabaseSchemaAgent(),
        ]

        for agent in default_agents:
            self.register(agent)

    def register(self, agent: BaseAgent) -> None:
        """
        Register an agent.

        Args:
            agent: Agent to register
        """
        self._agents[agent.name] = agent

    def get(self, name: str) -> Optional[BaseAgent]:
        """
        Get an agent by name.

        Args:
            name: Agent name

        Returns:
            Agent or None if not found
        """
        return self._agents.get(name)

    def list_all(self) -> List[Dict[str, Any]]:
        """
        List all registered agents.

        Returns:
            List of agent information
        """
        return [
            {
                "name": agent.name,
                "description": agent.description,
                "skills": agent._list_skills()
            }
            for agent in self._agents.values()
        ]

    def get_by_capability(self, capability: str) -> List[BaseAgent]:
        """
        Get agents by capability.

        Args:
            capability: Capability keyword (e.g., "backend", "auth", "database")

        Returns:
            List of matching agents
        """
        matches = []

        for agent in self._agents.values():
            if capability.lower() in agent.name.lower() or capability.lower() in agent.description.lower():
                matches.append(agent)

        return matches


# Global registry instance
registry = AgentRegistry()


def get_agent(name: str) -> Optional[BaseAgent]:
    """
    Get an agent from the global registry.

    Args:
        name: Agent name

    Returns:
        Agent or None if not found

    Example:
        >>> from intelligence.registry import get_agent
        >>> agent = get_agent("RAG-Knowledge-Agent")
    """
    return registry.get(name)


def list_agents() -> List[Dict[str, Any]]:
    """
    List all agents in the global registry.

    Returns:
        List of agent information

    Example:
        >>> from intelligence.registry import list_agents
        >>> agents = list_agents()
        >>> for agent in agents:
        ...     print(f"{agent['name']}: {agent['description']}")
    """
    return registry.list_all()
