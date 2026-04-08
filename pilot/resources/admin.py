"""Admin resource — user management, invites, stats, settings."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pilot.models import Invite, Stats, User

if TYPE_CHECKING:
    from pilot.client import PilotClient


class AdminResource:
    """Admin operations: users, invites, stats, and settings."""

    def __init__(self, client: PilotClient) -> None:
        self._client = client

    def users(self) -> list[User]:
        """List all users.

        Returns:
            List of User objects.
        """
        data = self._client._request("GET", "/api/v1/admin/users")
        items = data if isinstance(data, list) else data.get("users", data.get("items", []))
        return [User.from_api(u) for u in items]

    def update_user(self, user_id: str, **fields: Any) -> dict[str, Any]:
        """Update a user (e.g. change plan or deactivate).

        Args:
            user_id: The user ID.
            **fields: Fields to update (e.g. plan='pro', is_active=False).

        Returns:
            Raw API response dict.
        """
        return self._client._request("PATCH", f"/api/v1/admin/users/{user_id}", json=fields)

    def invite(self, *, email: str | None = None, note: str | None = None) -> Invite:
        """Create an invite.

        Args:
            email: Pre-assign the invite to this email (optional).
            note: Internal note about the invite (optional).

        Returns:
            The created Invite with its code.
        """
        payload: dict[str, str] = {}
        if email is not None:
            payload["email"] = email
        if note is not None:
            payload["note"] = note
        data = self._client._request("POST", "/api/v1/admin/invite", json=payload)
        return Invite.from_api(data)

    def invites(self) -> list[Invite]:
        """List all invites.

        Returns:
            List of Invite objects.
        """
        data = self._client._request("GET", "/api/v1/admin/invites")
        items = data if isinstance(data, list) else data.get("invites", data.get("items", []))
        return [Invite.from_api(i) for i in items]

    def stats(self) -> Stats:
        """Get admin dashboard stats.

        Returns:
            Stats object (access data via .raw dict).
        """
        data = self._client._request("GET", "/api/v1/admin/stats")
        return Stats.from_api(data)

    def settings(self) -> dict[str, Any]:
        """Get current admin settings.

        Returns:
            Settings as a dict.
        """
        return self._client._request("GET", "/api/v1/admin/settings")

    def update_settings(self, settings: dict[str, Any]) -> dict[str, Any]:
        """Update admin settings.

        Args:
            settings: Dict of setting key-value pairs.

        Returns:
            Raw API response dict.
        """
        return self._client._request(
            "POST", "/api/v1/admin/settings", json={"settings": settings}
        )
