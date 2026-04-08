"""RPM resource — Results / Purpose / Massive Action Plan projects."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pilot.models import RPMProject

if TYPE_CHECKING:
    from pilot.client import PilotClient


class RPMResource:
    """Manage RPM (Tony Robbins methodology) projects."""

    def __init__(self, client: PilotClient) -> None:
        self._client = client

    def list(self, *, status: str | None = None) -> list[RPMProject]:
        """List RPM projects, optionally filtered by status.

        Args:
            status: Filter by status (e.g. 'active', 'completed').

        Returns:
            List of RPMProject objects.
        """
        params: dict[str, str] = {}
        if status is not None:
            params["status"] = status
        data = self._client._request("GET", "/api/v1/rpm", params=params)
        items = data if isinstance(data, list) else data.get("projects", data.get("items", []))
        return [RPMProject.from_api(p) for p in items]

    def get(self, project_id: str) -> RPMProject:
        """Get a specific RPM project.

        Args:
            project_id: The project ID.

        Returns:
            RPMProject object.
        """
        data = self._client._request("GET", f"/api/v1/rpm/{project_id}")
        return RPMProject.from_api(data)

    def create(
        self,
        result: str,
        purpose: str,
        *,
        massive_action_plan: list[str] | None = None,
        status: str = "active",
        priority: int = 0,
        due_date: str | None = None,
    ) -> RPMProject:
        """Create a new RPM project.

        Args:
            result: The desired result.
            purpose: Why this result matters.
            massive_action_plan: List of action steps (optional).
            status: Initial status (default 'active').
            priority: Priority level (default 0).
            due_date: Due date as ISO string (optional).

        Returns:
            The created RPMProject.
        """
        payload: dict[str, Any] = {
            "result": result,
            "purpose": purpose,
            "status": status,
            "priority": priority,
        }
        if massive_action_plan is not None:
            payload["massive_action_plan"] = massive_action_plan
        if due_date is not None:
            payload["due_date"] = due_date
        data = self._client._request("POST", "/api/v1/rpm", json=payload)
        return RPMProject.from_api(data)

    def update(self, project_id: str, **fields: Any) -> dict[str, Any]:
        """Update an RPM project.

        Args:
            project_id: The project ID.
            **fields: Fields to update (result, purpose, massive_action_plan, status, priority, due_date).

        Returns:
            Raw API response dict.
        """
        return self._client._request("PUT", f"/api/v1/rpm/{project_id}", json=fields)

    def delete(self, project_id: str) -> dict[str, Any]:
        """Delete an RPM project.

        Args:
            project_id: The project ID.

        Returns:
            Raw API response dict.
        """
        return self._client._request("DELETE", f"/api/v1/rpm/{project_id}")
