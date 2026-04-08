"""Decisions resource — decision logging and search."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pilot.models import Decision

if TYPE_CHECKING:
    from pilot.client import PilotClient


class DecisionsResource:
    """Log, search, and manage decisions."""

    def __init__(self, client: PilotClient) -> None:
        self._client = client

    def list(self) -> list[Decision]:
        """List all decisions.

        Returns:
            List of Decision objects.
        """
        data = self._client._request("GET", "/api/v1/decisions")
        items = data if isinstance(data, list) else data.get("decisions", data.get("items", []))
        return [Decision.from_api(d) for d in items]

    def create(
        self,
        title: str,
        *,
        context: str = "",
        rationale: str = "",
        outcome: str | None = None,
    ) -> Decision:
        """Log a new decision.

        Args:
            title: Short title of the decision.
            context: Background/context for the decision.
            rationale: Why this decision was made.
            outcome: Expected or actual outcome (optional).

        Returns:
            The created Decision.
        """
        payload: dict[str, Any] = {"title": title}
        if context:
            payload["context"] = context
        if rationale:
            payload["rationale"] = rationale
        if outcome is not None:
            payload["outcome"] = outcome
        data = self._client._request("POST", "/api/v1/decisions", json=payload)
        return Decision.from_api(data)

    def update(self, decision_id: str, **fields: Any) -> dict[str, Any]:
        """Update a decision.

        Args:
            decision_id: The decision ID.
            **fields: Fields to update (title, context, rationale, outcome).

        Returns:
            Raw API response dict.
        """
        return self._client._request("PUT", f"/api/v1/decisions/{decision_id}", json=fields)

    def search(self, query: str) -> list[Decision]:
        """Search decisions.

        Args:
            query: Search query string.

        Returns:
            List of matching Decision objects.
        """
        data = self._client._request("GET", "/api/v1/decisions/search", params={"q": query})
        items = data if isinstance(data, list) else data.get("results", data.get("decisions", []))
        return [Decision.from_api(d) for d in items]
