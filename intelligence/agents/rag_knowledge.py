"""
RAG Knowledge Agent

Agent specialized in retrieval-augmented generation for documentation and specifications.
"""

from typing import Dict, Any, List, Optional
from .base import BaseAgent
from ..skills import RAGSkills


class RAGKnowledgeAgent(BaseAgent):
    """Agent for knowledge retrieval and documentation assistance."""

    def __init__(self):
        """Initialize RAG Knowledge Agent."""
        super().__init__(
            name="RAG-Knowledge-Agent",
            description="Retrieves documentation and provides architecture guidance using Context7 MCP and local specs"
        )
        self.skills = RAGSkills()

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a knowledge retrieval task.

        Args:
            task: Task specification with 'skill' and 'params'

        Returns:
            Task result

        Example:
            >>> agent = RAGKnowledgeAgent()
            >>> result = agent.execute({
            ...     "skill": "retrieve_docs",
            ...     "params": {"library": "fastapi", "topic": "authentication"}
            ... })
        """
        skill = task.get("skill")
        params = task.get("params", {})

        if skill == "retrieve_docs":
            result = self.skills.retrieve_docs(**params)

        elif skill == "summarize_spec":
            result = self.skills.summarize_spec(**params)

        elif skill == "architecture_guidance":
            result = self.skills.architecture_guidance(**params)

        elif skill == "resolve_api_questions":
            result = self.skills.resolve_api_questions(**params)

        elif skill == "get_database_schema":
            result = self.skills.get_database_schema()

        else:
            result = {
                "error": f"Unknown skill: {skill}",
                "available_skills": self._list_skills()
            }

        self.log_execution(task, result)
        return result

    def retrieve_docs(
        self,
        library: str,
        topic: Optional[str] = None,
        mode: str = "code"
    ) -> Dict[str, Any]:
        """
        Retrieve documentation for a library.

        Args:
            library: Library name
            topic: Specific topic
            mode: "code" or "info"

        Returns:
            Documentation content
        """
        return self.execute({
            "skill": "retrieve_docs",
            "params": {"library": library, "topic": topic, "mode": mode}
        })

    def summarize_spec(self, feature_name: str) -> Dict[str, Any]:
        """
        Summarize a feature specification.

        Args:
            feature_name: Feature name

        Returns:
            Specification summary
        """
        return self.execute({
            "skill": "summarize_spec",
            "params": {"feature_name": feature_name}
        })

    def architecture_guidance(self, question: str) -> Dict[str, Any]:
        """
        Get architecture guidance.

        Args:
            question: Architecture question

        Returns:
            Guidance from constitution
        """
        return self.execute({
            "skill": "architecture_guidance",
            "params": {"question": question}
        })

    def resolve_api_questions(self, endpoint_pattern: str) -> Dict[str, Any]:
        """
        Resolve API endpoint questions.

        Args:
            endpoint_pattern: Endpoint pattern to search

        Returns:
            API endpoint information
        """
        return self.execute({
            "skill": "resolve_api_questions",
            "params": {"endpoint_pattern": endpoint_pattern}
        })

    def _list_skills(self) -> List[str]:
        """List available skills."""
        return [
            "retrieve_docs",
            "summarize_spec",
            "architecture_guidance",
            "resolve_api_questions",
            "get_database_schema"
        ]
