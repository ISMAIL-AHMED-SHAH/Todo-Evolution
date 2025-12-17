"""
RAG (Retrieval-Augmented Generation) Skills

Skills for retrieving and working with documentation and specifications.
"""

from typing import Dict, Any, List, Optional
from ..tools import Context7Client, SpecLoader


class RAGSkills:
    """Skills for knowledge retrieval and documentation assistance."""

    def __init__(self):
        """Initialize RAG skills."""
        self.context7 = Context7Client()
        self.spec_loader = SpecLoader()

    def retrieve_docs(
        self,
        library: str,
        topic: Optional[str] = None,
        mode: str = "code"
    ) -> Dict[str, Any]:
        """
        Retrieve documentation for a library.

        Args:
            library: Library name (e.g., "fastapi", "nextjs")
            topic: Specific topic to focus on
            mode: "code" for API references, "info" for guides

        Returns:
            Documentation content

        Example:
            >>> skills = RAGSkills()
            >>> docs = skills.retrieve_docs("fastapi", topic="authentication")
        """
        library_id = self.context7.resolve_library_id(library)

        if not library_id:
            return {
                "error": f"Library '{library}' not found",
                "suggestion": "Check library name spelling"
            }

        return self.context7.get_library_docs(
            library_id=library_id,
            topic=topic,
            mode=mode
        )

    def summarize_spec(self, feature_name: str) -> Dict[str, Any]:
        """
        Summarize a feature specification.

        Args:
            feature_name: Name of the feature

        Returns:
            Summary of the specification

        Example:
            >>> skills = RAGSkills()
            >>> summary = skills.summarize_spec("1-fullstack-web-app")
        """
        try:
            spec = self.spec_loader.load_spec(feature_name)

            summary = {
                "feature": spec["feature"],
                "status": spec["metadata"].get("status", "Unknown"),
                "user_stories": self._extract_user_stories(spec["content"]),
                "requirements": self._extract_requirements(spec["content"]),
            }

            return summary

        except FileNotFoundError as e:
            return {"error": str(e)}

    def architecture_guidance(self, question: str) -> Dict[str, Any]:
        """
        Provide architecture guidance based on constitution and specs.

        Args:
            question: Architecture question

        Returns:
            Guidance based on project constitution

        Example:
            >>> skills = RAGSkills()
            >>> guidance = skills.architecture_guidance("What authentication method should I use?")
        """
        try:
            constitution = self.spec_loader.load_constitution()

            relevant_principles = []

            # Search for relevant principles
            for principle in constitution["principles"]:
                if any(keyword in principle["content"].lower() for keyword in ["auth", "jwt", "token", "security"]):
                    relevant_principles.append(principle)

            return {
                "question": question,
                "relevant_principles": relevant_principles,
                "constitution_path": constitution["path"]
            }

        except FileNotFoundError as e:
            return {"error": str(e)}

    def resolve_api_questions(self, endpoint_pattern: str) -> Dict[str, Any]:
        """
        Resolve questions about API endpoints.

        Args:
            endpoint_pattern: Pattern to search for (e.g., "/tasks", "GET")

        Returns:
            API endpoint information

        Example:
            >>> skills = RAGSkills()
            >>> info = skills.resolve_api_questions("/tasks")
        """
        try:
            api_contract = self.spec_loader.load_api_contract()

            matching_endpoints = [
                ep for ep in api_contract["endpoints"]
                if endpoint_pattern.lower() in ep["path"].lower()
                or endpoint_pattern.upper() == ep["method"]
            ]

            return {
                "pattern": endpoint_pattern,
                "matching_endpoints": matching_endpoints,
                "contract_path": api_contract["path"]
            }

        except FileNotFoundError as e:
            return {"error": str(e)}

    def get_database_schema(self) -> Dict[str, Any]:
        """
        Retrieve database schema information.

        Returns:
            Database schema details

        Example:
            >>> skills = RAGSkills()
            >>> schema = skills.get_database_schema()
        """
        try:
            schema = self.spec_loader.load_database_schema()

            return {
                "entities": schema["entities"],
                "schema_path": schema["path"],
                "content_preview": schema["content"][:500]
            }

        except FileNotFoundError as e:
            return {"error": str(e)}

    def _extract_user_stories(self, content: str) -> List[str]:
        """Extract user story titles from content."""
        import re

        stories = []
        pattern = r'###\s+User Story \d+\s+-\s+(.+)'

        for match in re.finditer(pattern, content):
            stories.append(match.group(1).strip())

        return stories

    def _extract_requirements(self, content: str) -> List[str]:
        """Extract functional requirements from content."""
        import re

        requirements = []
        pattern = r'-\s+\*\*FR-\d+\*\*:\s+(.+)'

        for match in re.finditer(pattern, content):
            requirements.append(match.group(1).strip())

        return requirements
