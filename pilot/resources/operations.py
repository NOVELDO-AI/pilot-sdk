"""Operations resource — recurring and one-off operational tasks."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pilot.models import Operation

if TYPE_CHECKING:
    from pilot.client import PilotClient


class OperationsResource:
    """Manage operations (recurring admin tasks, processes)."""

    def __init__(self, client: PilotClient) -> None:
        self._client = client

    def list(
        self,
        *,
        category: str | None = None,
        status: str | None = None,
    ) -> list[Operation]:
        """List operations, optionally filtered.

        Args:
            category: Filter by category (e.g. 'admin', 'finance').
            status: Filter by status (e.g. 'pending', 'done').

        Returns:
            List of Operation objects.
        """
        params: dict[str, str] = {}
        if category is not None:
            params["category"] = category
        if status is not None:
            params["status"] = status
        data = self._client._request("GET", "/api/v1/operations", params=params)
        items = data if isinstance(data, list) else data.get("operations", data.get("items", []))
        return [Operation.from_api(o) for o in items]

    def create(
        self,
        title: str,
        *,
        description: str = "",
        category: str = "admin",
        due_date: str | None = None,
        recurrence: str = "one-off",
        status: str = "pending",
    ) -> Operation:
        """Create a new operation.

        Args:
            title: Operation title.
            description: Details about the operation.
            category: Category (default 'admin').
            due_date: Due date as ISO string (optional).
            recurrence: Recurrence pattern (default 'one-off').
            status: Initial status (default 'pending').

        Returns:
            The created Operation.
        """
        payload: dict[str, Any] = {
            "title": title,
            "category": category,
            "recurrence": recurrence,
            "status": status,
        }
        if description:
            payload["description"] = description
        if due_date is not None:
            payload["due_date"] = due_date
        data = self._client._request("POST", "/api/v1/operations", json=payload)
        return Operation.from_api(data)

    def update(self, op_id: str, **fields: Any) -> dict[str, Any]:
        """Update an operation.

        Args:
            op_id: The operation ID.
            **fields: Fields to update.

        Returns:
            Raw API response dict.
        """
        return self._client._request("PUT", f"/api/v1/operations/{op_id}", json=fields)

    def delete(self, op_id: str) -> dict[str, Any]:
        """Delete an operation.

        Args:
            op_id: The operation ID.

        Returns:
            Raw API response dict.
        """
        return self._client._request("DELETE", f"/api/v1/operations/{op_id}")
