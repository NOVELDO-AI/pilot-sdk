"""PILOT Python SDK — AI Chief of Staff API client."""

from __future__ import annotations

from typing import Any

import httpx

from pilot.exceptions import (
    AuthenticationError,
    NotFoundError,
    PilotError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from pilot.resources.admin import AdminResource
from pilot.resources.briefing import BriefingResource
from pilot.resources.capture import CaptureResource
from pilot.resources.chat import ChatResource
from pilot.resources.decisions import DecisionsResource
from pilot.resources.delegations import DelegationsResource
from pilot.resources.email import EmailResource
from pilot.resources.graph import GraphResource
from pilot.resources.operations import OperationsResource
from pilot.resources.rpm import RPMResource
from pilot.resources.someday import SomedayResource
from pilot.resources.tasks import TasksResource

_DEFAULT_BASE_URL = "https://app.withpilot.ai"


class PilotClient:
    """Client for the PILOT API.

    Usage::

        from pilot import PilotClient

        client = PilotClient(api_key="pk_live_...")
        briefing = client.briefing.get()
        reply = client.chat.send("What should I focus on today?")

    Supports both API keys (``pk_live_...``) and JWT tokens.
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = 30.0,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Initialize the PILOT client.

        Args:
            api_key: API key (``pk_live_...``) or JWT bearer token.
            base_url: API base URL (default ``https://app.withpilot.ai``).
            timeout: Request timeout in seconds.
            headers: Additional headers to include on every request.
        """
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")

        default_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "pilot-sdk-python/0.1.0",
        }
        if headers:
            default_headers.update(headers)

        self._http = httpx.Client(
            base_url=self._base_url,
            headers=default_headers,
            timeout=timeout,
        )

        # Resource instances (lazy init)
        self._briefing: BriefingResource | None = None
        self._chat: ChatResource | None = None
        self._email: EmailResource | None = None
        self._delegations: DelegationsResource | None = None
        self._graph: GraphResource | None = None
        self._tasks: TasksResource | None = None
        self._admin: AdminResource | None = None
        self._capture: CaptureResource | None = None
        self._decisions: DecisionsResource | None = None
        self._rpm: RPMResource | None = None
        self._operations: OperationsResource | None = None
        self._someday: SomedayResource | None = None

    # ── Resource accessors ───────────────────────────────────────────

    @property
    def briefing(self) -> BriefingResource:
        """Morning briefing and weekly review endpoints."""
        if self._briefing is None:
            self._briefing = BriefingResource(self)
        return self._briefing

    @property
    def chat(self) -> ChatResource:
        """Chat / conversational endpoints."""
        if self._chat is None:
            self._chat = ChatResource(self)
        return self._chat

    @property
    def email(self) -> EmailResource:
        """Email triage, drafting, and batch operations."""
        if self._email is None:
            self._email = EmailResource(self)
        return self._email

    @property
    def delegations(self) -> DelegationsResource:
        """Delegation tracking endpoints."""
        if self._delegations is None:
            self._delegations = DelegationsResource(self)
        return self._delegations

    @property
    def graph(self) -> GraphResource:
        """Knowledge graph queries."""
        if self._graph is None:
            self._graph = GraphResource(self)
        return self._graph

    @property
    def tasks(self) -> TasksResource:
        """Task management endpoints."""
        if self._tasks is None:
            self._tasks = TasksResource(self)
        return self._tasks

    @property
    def admin(self) -> AdminResource:
        """Admin: users, invites, stats, settings."""
        if self._admin is None:
            self._admin = AdminResource(self)
        return self._admin

    @property
    def capture(self) -> CaptureResource:
        """Raw input capture and inbox."""
        if self._capture is None:
            self._capture = CaptureResource(self)
        return self._capture

    @property
    def decisions(self) -> DecisionsResource:
        """Decision logging and search."""
        if self._decisions is None:
            self._decisions = DecisionsResource(self)
        return self._decisions

    @property
    def rpm(self) -> RPMResource:
        """RPM (Results / Purpose / Massive Action Plan) projects."""
        if self._rpm is None:
            self._rpm = RPMResource(self)
        return self._rpm

    @property
    def operations(self) -> OperationsResource:
        """Recurring and one-off operations."""
        if self._operations is None:
            self._operations = OperationsResource(self)
        return self._operations

    @property
    def someday(self) -> SomedayResource:
        """Someday/maybe list."""
        if self._someday is None:
            self._someday = SomedayResource(self)
        return self._someday

    # ── HTTP plumbing ────────────────────────────────────────────────

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        """Send an HTTP request and return parsed JSON.

        Raises appropriate PilotError subclasses on failure.
        """
        response = self._http.request(method, path, params=params, json=json)
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response: httpx.Response) -> Any:
        """Parse response, raising typed errors on non-2xx status codes."""
        if response.is_success:
            if not response.content:
                return {}
            return response.json()

        # Try to get error body
        body: dict[str, Any] = {}
        try:
            body = response.json()
        except Exception:
            pass

        message = body.get("detail", body.get("message", response.text[:200]))
        status = response.status_code

        if status in (401, 403):
            raise AuthenticationError(f"Authentication failed: {message}", status, body)
        if status == 404:
            raise NotFoundError(f"Not found: {message}", status, body)
        if status == 422:
            raise ValidationError(f"Validation error: {message}", status, body)
        if status == 429:
            raise RateLimitError(f"Rate limit exceeded: {message}", status, body)
        if status >= 500:
            raise ServerError(f"Server error ({status}): {message}", status, body)

        raise PilotError(f"API error ({status}): {message}", status, body)

    # ── Context manager ──────────────────────────────────────────────

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._http.close()

    def __enter__(self) -> PilotClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"PilotClient(base_url={self._base_url!r})"
