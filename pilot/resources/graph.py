"""Graph resource — knowledge graph queries."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pilot.models import GraphData, GraphEdge, GraphNode

if TYPE_CHECKING:
    from pilot.client import PilotClient


class GraphResource:
    """Query and navigate the PILOT knowledge graph."""

    def __init__(self, client: PilotClient) -> None:
        self._client = client

    def get(self) -> GraphData:
        """Fetch the full graph (nodes + edges).

        Returns:
            GraphData with nodes and edges.
        """
        data = self._client._request("GET", "/api/v1/graph")
        return GraphData.from_api(data)

    def search(self, query: str) -> list[GraphNode]:
        """Search the knowledge graph.

        Args:
            query: Search query string.

        Returns:
            List of matching GraphNode objects.
        """
        data = self._client._request("GET", "/api/v1/graph/search", params={"q": query})
        items = data if isinstance(data, list) else data.get("results", data.get("nodes", []))
        return [GraphNode.from_api(n) for n in items]

    def node(self, node_id: str, *, depth: int | None = None) -> GraphNode:
        """Get a specific node by ID.

        Args:
            node_id: The node ID.
            depth: How many relationship hops to include.

        Returns:
            GraphNode with properties.
        """
        params: dict[str, str] = {}
        if depth is not None:
            params["depth"] = str(depth)
        data = self._client._request("GET", f"/api/v1/graph/node/{node_id}", params=params)
        return GraphNode.from_api(data)

    def pin(self, node_id: str) -> dict[str, Any]:
        """Pin a node for quick access.

        Args:
            node_id: The node ID to pin.

        Returns:
            Raw API response dict.
        """
        return self._client._request("POST", f"/api/v1/graph/node/{node_id}/pin")

    def unpin(self, node_id: str) -> dict[str, Any]:
        """Unpin a node.

        Args:
            node_id: The node ID to unpin.

        Returns:
            Raw API response dict.
        """
        return self._client._request("DELETE", f"/api/v1/graph/node/{node_id}/pin")

    def relationships(self) -> list[GraphEdge]:
        """Fetch all relationships in the graph.

        Returns:
            List of GraphEdge objects.
        """
        data = self._client._request("GET", "/api/v1/graph/relationships")
        items = data if isinstance(data, list) else data.get("relationships", data.get("edges", []))
        return [GraphEdge.from_api(e) for e in items]

    def person(self, label: str) -> dict[str, Any]:
        """Get person details by label.

        Args:
            label: The person label/name.

        Returns:
            Raw API response dict with person details.
        """
        return self._client._request("GET", f"/api/v1/graph/person/{label}")

    def project(self, label: str) -> dict[str, Any]:
        """Get project details by label.

        Args:
            label: The project label/name.

        Returns:
            Raw API response dict with project details.
        """
        return self._client._request("GET", f"/api/v1/graph/project/{label}")
