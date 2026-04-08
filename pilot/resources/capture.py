"""Capture resource — raw input capture and inbox management."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pilot.models import CaptureEvent

if TYPE_CHECKING:
    from pilot.client import PilotClient


class CaptureResource:
    """Capture raw input and manage the inbox."""

    def __init__(self, client: PilotClient) -> None:
        self._client = client

    def create(
        self,
        content: str,
        *,
        source: str = "sdk",
        sender: str | None = None,
        attachments: list[dict[str, Any]] | None = None,
    ) -> CaptureEvent:
        """Capture raw text input for classification.

        Args:
            content: The text to capture.
            source: Source identifier (default 'sdk').
            sender: Who sent it (optional).
            attachments: List of attachment dicts (optional).

        Returns:
            The created CaptureEvent.
        """
        payload: dict[str, Any] = {"content": content, "source": source}
        if sender is not None:
            payload["sender"] = sender
        if attachments is not None:
            payload["attachments"] = attachments
        data = self._client._request("POST", "/api/v1/capture", json=payload)
        return CaptureEvent.from_api(data)

    def inbox(self) -> list[CaptureEvent]:
        """List unprocessed or low-confidence captures.

        Returns:
            List of CaptureEvent objects.
        """
        data = self._client._request("GET", "/api/v1/inbox")
        items = data if isinstance(data, list) else data.get("items", [])
        return [CaptureEvent.from_api(c) for c in items]

    def route(self, capture_id: str, tier: int, fields: dict[str, Any]) -> dict[str, Any]:
        """Manually route a capture to a tier.

        Args:
            capture_id: The capture event ID.
            tier: The tier number to route to.
            fields: Fields required by that tier.

        Returns:
            Raw API response dict.
        """
        return self._client._request(
            "POST",
            f"/api/v1/inbox/{capture_id}/route",
            json={"tier": tier, "fields": fields},
        )
