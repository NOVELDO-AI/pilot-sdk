"""Someday resource — someday/maybe list management."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pilot.models import SomedayItem

if TYPE_CHECKING:
    from pilot.client import PilotClient


class SomedayResource:
    """Manage the someday/maybe list."""

    def __init__(self, client: PilotClient) -> None:
        self._client = client

    def list(self, *, area: str | None = None, query: str | None = None) -> list[SomedayItem]:
        """List someday/maybe items.

        Args:
            area: Filter by area (optional).
            query: Search query (optional).

        Returns:
            List of SomedayItem objects.
        """
        params: dict[str, str] = {}
        if area is not None:
            params["area"] = area
        if query is not None:
            params["q"] = query
        data = self._client._request("GET", "/api/v1/someday", params=params)
        items = data if isinstance(data, list) else data.get("items", [])
        return [SomedayItem.from_api(s) for s in items]

    def create(self, title: str, *, description: str = "", area: str = "other") -> SomedayItem:
        """Add a someday/maybe item.

        Args:
            title: Item title.
            description: Details (optional).
            area: Area/category (default 'other').

        Returns:
            The created SomedayItem.
        """
        payload: dict[str, str] = {"title": title, "area": area}
        if description:
            payload["description"] = description
        data = self._client._request("POST", "/api/v1/someday", json=payload)
        return SomedayItem.from_api(data)

    def update(self, item_id: str, **fields: Any) -> dict[str, Any]:
        """Update a someday/maybe item.

        Args:
            item_id: The item ID.
            **fields: Fields to update (title, description, area).

        Returns:
            Raw API response dict.
        """
        return self._client._request("PUT", f"/api/v1/someday/{item_id}", json=fields)

    def delete(self, item_id: str) -> dict[str, Any]:
        """Delete a someday/maybe item.

        Args:
            item_id: The item ID.

        Returns:
            Raw API response dict.
        """
        return self._client._request("DELETE", f"/api/v1/someday/{item_id}")
