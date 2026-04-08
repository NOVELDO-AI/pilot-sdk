"""Email resource — triage, drafting, sending, and batch operations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pilot.models import DraftReply, EmailThread, TriagedEmail

if TYPE_CHECKING:
    from pilot.client import PilotClient


class EmailResource:
    """Manage email triage, replies, and batch operations."""

    def __init__(self, client: PilotClient) -> None:
        self._client = client

    def triage(self, *, limit: int = 30) -> list[TriagedEmail]:
        """Fetch triaged emails.

        Args:
            limit: Maximum number of emails to return.

        Returns:
            List of triaged email summaries.
        """
        data = self._client._request("GET", "/api/v1/email/triage", params={"limit": str(limit)})
        items = data if isinstance(data, list) else data.get("emails", data.get("items", []))
        return [TriagedEmail.from_api(e) for e in items]

    def draft_reply(self, message_id: str, *, tone: str = "professional") -> DraftReply:
        """Draft a reply to an email.

        Args:
            message_id: The ID of the message to reply to.
            tone: Tone of the reply (e.g. 'professional', 'casual', 'brief').

        Returns:
            DraftReply with the generated HTML body.
        """
        data = self._client._request(
            "POST",
            "/api/v1/email/draft-reply",
            json={"message_id": message_id, "tone": tone},
        )
        return DraftReply.from_api(data)

    def send_reply(self, message_id: str, body_html: str) -> dict[str, Any]:
        """Send a reply to an email.

        Args:
            message_id: The ID of the message to reply to.
            body_html: The HTML body of the reply.

        Returns:
            Raw API response dict.
        """
        return self._client._request(
            "POST",
            "/api/v1/email/send-reply",
            json={"message_id": message_id, "body_html": body_html},
        )

    def unanswered(self, *, days: int = 3) -> list[TriagedEmail]:
        """Fetch unanswered emails.

        Args:
            days: Look back this many days for unanswered emails.

        Returns:
            List of unanswered email summaries.
        """
        data = self._client._request("GET", "/api/v1/email/unanswered", params={"days": str(days)})
        items = data if isinstance(data, list) else data.get("emails", data.get("items", []))
        return [TriagedEmail.from_api(e) for e in items]

    def thread(self, conversation_id: str) -> EmailThread:
        """Fetch a full email thread.

        Args:
            conversation_id: The conversation/thread ID.

        Returns:
            EmailThread with all messages.
        """
        data = self._client._request("GET", f"/api/v1/email/thread/{conversation_id}")
        return EmailThread.from_api(data)

    def delegate(self, message_id: str, to_address: str, *, comment: str = "") -> dict[str, Any]:
        """Delegate an email to someone else.

        Args:
            message_id: The message to delegate.
            to_address: Email address of the delegate.
            comment: Optional comment/instructions.

        Returns:
            Raw API response dict.
        """
        payload: dict[str, str] = {"message_id": message_id, "to_address": to_address}
        if comment:
            payload["comment"] = comment
        return self._client._request("POST", "/api/v1/email/delegate", json=payload)

    def batch_archive(self, message_ids: list[str]) -> dict[str, Any]:
        """Archive multiple emails at once.

        Args:
            message_ids: List of message IDs to archive.

        Returns:
            Raw API response dict.
        """
        return self._client._request(
            "POST", "/api/v1/email/batch/archive", json={"message_ids": message_ids}
        )

    def batch_read(self, message_ids: list[str]) -> dict[str, Any]:
        """Mark multiple emails as read.

        Args:
            message_ids: List of message IDs to mark as read.

        Returns:
            Raw API response dict.
        """
        return self._client._request(
            "POST", "/api/v1/email/batch/read", json={"message_ids": message_ids}
        )
