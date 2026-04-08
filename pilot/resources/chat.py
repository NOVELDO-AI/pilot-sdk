"""Chat resource — conversational interaction with PILOT."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pilot.models import ChatResponse

if TYPE_CHECKING:
    from pilot.client import PilotClient


class ChatResource:
    """Send messages and have conversations with PILOT."""

    def __init__(self, client: PilotClient) -> None:
        self._client = client
        self._history: list[dict[str, str]] = []

    def send(
        self,
        message: str,
        *,
        history: list[dict[str, str]] | None = None,
        remember: bool = True,
    ) -> str:
        """Send a message to PILOT and get a reply.

        Args:
            message: The user message to send.
            history: Explicit conversation history. If None, uses internal history.
            remember: Whether to append this exchange to internal history (default True).

        Returns:
            The assistant's reply as a string.
        """
        messages = history if history is not None else list(self._history)
        messages.append({"role": "user", "content": message})

        data = self._client._request("POST", "/api/v1/chat", json={"messages": messages})
        response = ChatResponse(**data)

        if remember:
            self._history.append({"role": "user", "content": message})
            self._history.append({"role": "assistant", "content": response.reply})

        return response.reply

    def clear_history(self) -> None:
        """Clear the internal conversation history."""
        self._history.clear()
