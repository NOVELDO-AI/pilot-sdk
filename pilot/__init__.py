"""PILOT Python SDK — AI Chief of Staff API client.

Usage::

    from pilot import PilotClient

    client = PilotClient(api_key="pk_live_...")
    briefing = client.briefing.get()
    reply = client.chat.send("What should I focus on today?")
"""

from pilot.client import PilotClient
from pilot.exceptions import (
    AuthenticationError,
    NotFoundError,
    PilotError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from pilot.models import (
    APIKey,
    Briefing,
    CaptureEvent,
    ChatResponse,
    Decision,
    Delegation,
    DraftReply,
    EmailThread,
    FocusItem,
    GraphData,
    GraphEdge,
    GraphNode,
    Invite,
    Operation,
    RPMProject,
    SomedayItem,
    Stats,
    Task,
    ThreadMessage,
    TriagedEmail,
    User,
    WeeklyReview,
)

__version__ = "0.1.0"

__all__ = [
    # Client
    "PilotClient",
    # Exceptions
    "AuthenticationError",
    "NotFoundError",
    "PilotError",
    "RateLimitError",
    "ServerError",
    "ValidationError",
    # Models
    "APIKey",
    "Briefing",
    "CaptureEvent",
    "ChatResponse",
    "Decision",
    "Delegation",
    "DraftReply",
    "EmailThread",
    "FocusItem",
    "GraphData",
    "GraphEdge",
    "GraphNode",
    "Invite",
    "Operation",
    "RPMProject",
    "SomedayItem",
    "Stats",
    "Task",
    "ThreadMessage",
    "TriagedEmail",
    "User",
    "WeeklyReview",
]
