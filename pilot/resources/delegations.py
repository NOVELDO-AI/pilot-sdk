"""Delegations resource — track delegated items."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pilot.models import Delegation

if TYPE_CHECKING:
    from pilot.client import PilotClient


class DelegationsResource:
    """Manage delegated items and their statuses."""

    def __init__(self, client: PilotClient) -> None:
        self._client = client

    def list(self, *, status: str | None = None) -> list[Delegation]:
        """List delegations, optionally filtered by status.

        Args:
            status: Filter by status (e.g. 'waiting', 'done').

        Returns:
            List of Delegation objects.
        """
        params: dict[str, str] = {}
        if status is not None:
            params["status"] = status
        data = self._client._request("GET", "/api/v1/delegations", params=params)
        items = data if isinstance(data, list) else data.get("delegations", data.get("items", []))
        return [Delegation.from_api(d) for d in items]

    def update(self, delegation_id: str, **fields: Any) -> dict[str, Any]:
        """Update a delegation (e.g. change status).

        Args:
            delegation_id: The delegation ID.
            **fields: Fields to update (e.g. status='done').

        Returns:
            Raw API response dict.
        """
        return self._client._request(
            "PATCH", f"/api/v1/delegations/{delegation_id}", json=fields
        )
