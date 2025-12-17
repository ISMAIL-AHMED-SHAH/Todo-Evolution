"""
Context7 MCP Client

Provides interface to Context7 MCP server for retrieving library documentation.
"""

from typing import Optional, Dict, Any, List
import json


class Context7Client:
    """Client for interacting with Context7 MCP server."""

    def __init__(self):
        """Initialize Context7 client."""
        self.cache: Dict[str, Any] = {}

    def resolve_library_id(self, library_name: str) -> Optional[str]:
        """
        Resolve a package/product name to a Context7-compatible library ID.

        Args:
            library_name: Name of the library to resolve (e.g., "fastapi", "nextjs")

        Returns:
            Context7-compatible library ID (e.g., "/tiangolo/fastapi")

        Example:
            >>> client = Context7Client()
            >>> client.resolve_library_id("fastapi")
            "/tiangolo/fastapi"
        """
        # This would normally call the MCP server
        # For now, provide common mappings
        library_mappings = {
            "fastapi": "/tiangolo/fastapi",
            "sqlmodel": "/tiangolo/sqlmodel",
            "nextjs": "/vercel/next.js",
            "next.js": "/vercel/next.js",
            "better-auth": "/better-auth/better-auth",
            "tailwindcss": "/tailwindlabs/tailwindcss",
        }

        return library_mappings.get(library_name.lower())

    def get_library_docs(
        self,
        library_id: str,
        topic: Optional[str] = None,
        mode: str = "code",
        page: int = 1
    ) -> Dict[str, Any]:
        """
        Fetch up-to-date documentation for a library.

        Args:
            library_id: Context7-compatible library ID (from resolve_library_id)
            topic: Topic to focus on (e.g., "authentication", "routing")
            mode: "code" for API references, "info" for conceptual guides
            page: Page number for pagination (1-10)

        Returns:
            Dictionary containing documentation content

        Example:
            >>> client = Context7Client()
            >>> docs = client.get_library_docs("/tiangolo/fastapi", topic="authentication")
        """
        cache_key = f"{library_id}:{topic}:{mode}:{page}"

        if cache_key in self.cache:
            return self.cache[cache_key]

        # This would normally call the MCP server
        # Return structure for integration
        result = {
            "library_id": library_id,
            "topic": topic,
            "mode": mode,
            "page": page,
            "content": [],
            "metadata": {}
        }

        self.cache[cache_key] = result
        return result

    def search_docs(
        self,
        library_id: str,
        query: str,
        mode: str = "code"
    ) -> List[Dict[str, Any]]:
        """
        Search documentation for specific content.

        Args:
            library_id: Context7-compatible library ID
            query: Search query
            mode: "code" or "info"

        Returns:
            List of search results
        """
        # Delegate to get_library_docs with topic
        docs = self.get_library_docs(library_id, topic=query, mode=mode)
        return docs.get("content", [])
