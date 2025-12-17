"""
Specification Loader

Loads and parses project specifications from the specs/ directory.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import re


class SpecLoader:
    """Loader for project specifications."""

    def __init__(self, specs_root: Optional[Path] = None):
        """
        Initialize specification loader.

        Args:
            specs_root: Root directory for specifications (defaults to ./specs)
        """
        self.specs_root = specs_root or Path("specs")

    def load_spec(self, feature_name: str) -> Dict[str, Any]:
        """
        Load specification for a feature.

        Args:
            feature_name: Name of the feature (e.g., "1-fullstack-web-app")

        Returns:
            Dictionary containing spec content and metadata
        """
        spec_path = self.specs_root / feature_name / "spec.md"

        if not spec_path.exists():
            raise FileNotFoundError(f"Spec not found: {spec_path}")

        content = spec_path.read_text(encoding="utf-8")

        return {
            "feature": feature_name,
            "path": str(spec_path),
            "content": content,
            "metadata": self._extract_metadata(content)
        }

    def load_plan(self, feature_name: str) -> Dict[str, Any]:
        """Load plan document for a feature."""
        plan_path = self.specs_root / feature_name / "plan.md"

        if not plan_path.exists():
            raise FileNotFoundError(f"Plan not found: {plan_path}")

        content = plan_path.read_text(encoding="utf-8")

        return {
            "feature": feature_name,
            "path": str(plan_path),
            "content": content,
            "metadata": self._extract_metadata(content)
        }

    def load_tasks(self, feature_name: str) -> Dict[str, Any]:
        """Load tasks document for a feature."""
        tasks_path = self.specs_root / feature_name / "tasks.md"

        if not tasks_path.exists():
            raise FileNotFoundError(f"Tasks not found: {tasks_path}")

        content = tasks_path.read_text(encoding="utf-8")

        return {
            "feature": feature_name,
            "path": str(tasks_path),
            "content": content,
            "tasks": self._extract_tasks(content),
            "metadata": self._extract_metadata(content)
        }

    def load_api_contract(self) -> Dict[str, Any]:
        """Load API contract specification."""
        api_path = self.specs_root / "api" / "rest-endpoints.md"

        if not api_path.exists():
            raise FileNotFoundError(f"API contract not found: {api_path}")

        content = api_path.read_text(encoding="utf-8")

        return {
            "path": str(api_path),
            "content": content,
            "endpoints": self._extract_endpoints(content)
        }

    def load_database_schema(self) -> Dict[str, Any]:
        """Load database schema specification."""
        schema_path = self.specs_root / "database" / "schema.md"

        if not schema_path.exists():
            # Try data-model.md as fallback
            schema_path = self.specs_root / "1-fullstack-web-app" / "data-model.md"

        if not schema_path.exists():
            raise FileNotFoundError("Database schema not found")

        content = schema_path.read_text(encoding="utf-8")

        return {
            "path": str(schema_path),
            "content": content,
            "entities": self._extract_entities(content)
        }

    def load_constitution(self) -> Dict[str, Any]:
        """Load project constitution."""
        constitution_path = Path(".specify/memory/constitution.md")

        if not constitution_path.exists():
            raise FileNotFoundError("Constitution not found")

        content = constitution_path.read_text(encoding="utf-8")

        return {
            "path": str(constitution_path),
            "content": content,
            "principles": self._extract_principles(content)
        }

    def _extract_metadata(self, content: str) -> Dict[str, str]:
        """Extract metadata from markdown frontmatter or header."""
        metadata = {}

        # Extract header metadata (e.g., **Feature**: name)
        feature_match = re.search(r'\*\*Feature\*\*:\s*(.+)', content)
        if feature_match:
            metadata["feature"] = feature_match.group(1).strip()

        status_match = re.search(r'\*\*Status\*\*:\s*(.+)', content)
        if status_match:
            metadata["status"] = status_match.group(1).strip()

        created_match = re.search(r'\*\*Created\*\*:\s*(.+)', content)
        if created_match:
            metadata["created"] = created_match.group(1).strip()

        return metadata

    def _extract_tasks(self, content: str) -> List[Dict[str, Any]]:
        """Extract task items from tasks document."""
        tasks = []

        # Match task items like: - [ ] T001 Task description
        task_pattern = r'-\s*\[([ x])\]\s*(T\d+)?\s*(.+)'

        for match in re.finditer(task_pattern, content):
            completed = match.group(1) == 'x'
            task_id = match.group(2)
            description = match.group(3).strip()

            tasks.append({
                "id": task_id,
                "description": description,
                "completed": completed
            })

        return tasks

    def _extract_endpoints(self, content: str) -> List[Dict[str, str]]:
        """Extract API endpoints from contract document."""
        endpoints = []

        # Match endpoint definitions like: #### GET /api/{user_id}/tasks
        endpoint_pattern = r'####\s+(GET|POST|PUT|PATCH|DELETE)\s+(/api/[^\s]+)'

        for match in re.finditer(endpoint_pattern, content):
            method = match.group(1)
            path = match.group(2)

            endpoints.append({
                "method": method,
                "path": path
            })

        return endpoints

    def _extract_entities(self, content: str) -> List[str]:
        """Extract entity names from schema document."""
        entities = []

        # Match entity definitions like: ### User Entity or ## User
        entity_pattern = r'###?\s+(\w+)\s+Entity'

        for match in re.finditer(entity_pattern, content):
            entity_name = match.group(1)
            if entity_name not in entities:
                entities.append(entity_name)

        return entities

    def _extract_principles(self, content: str) -> List[Dict[str, str]]:
        """Extract principles from constitution."""
        principles = []

        # Match principles like: ### I. Principle Title
        principle_pattern = r'###\s+([IVX]+)\.\s+(.+)'

        current_principle = None
        lines = content.split('\n')

        for i, line in enumerate(lines):
            match = re.match(principle_pattern, line)
            if match:
                if current_principle:
                    principles.append(current_principle)

                current_principle = {
                    "number": match.group(1),
                    "title": match.group(2).strip(),
                    "content": ""
                }
            elif current_principle and line.strip():
                current_principle["content"] += line + "\n"

        if current_principle:
            principles.append(current_principle)

        return principles
