"""Pydantic response models for the PILOT API."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ── Briefing ─────────────────────────────────────────────────────────

class FocusItem(BaseModel):
    """A single focus item inside a briefing."""
    title: str = ""
    detail: str = ""
    priority: str = ""


class Briefing(BaseModel):
    """Morning briefing response."""
    summary: str = ""
    focus_items: list[FocusItem] = Field(default_factory=list)
    raw: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Briefing:
        """Build from raw API dict, extracting known fields and preserving the rest."""
        focus_raw = data.get("focus_items") or data.get("focus") or []
        items = [FocusItem(**f) if isinstance(f, dict) else FocusItem(title=str(f)) for f in focus_raw]
        return cls(
            summary=data.get("summary", data.get("briefing", "")),
            focus_items=items,
            raw=data,
        )


class WeeklyReview(BaseModel):
    """Weekly accountability review."""
    review: str = ""
    raw: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> WeeklyReview:
        return cls(
            review=data.get("review", data.get("summary", "")),
            raw=data,
        )


# ── Chat ─────────────────────────────────────────────────────────────

class ChatResponse(BaseModel):
    """Response from the chat endpoint."""
    reply: str


# ── Email ────────────────────────────────────────────────────────────

class TriagedEmail(BaseModel):
    """A single triaged email message."""
    id: str = ""
    subject: str = ""
    sender: str = ""
    received_at: str = ""
    priority: str = ""
    summary: str = ""
    suggested_action: str = ""
    raw: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> TriagedEmail:
        return cls(
            id=data.get("id", data.get("message_id", "")),
            subject=data.get("subject", ""),
            sender=data.get("sender", data.get("from", "")),
            received_at=data.get("received_at", data.get("receivedDateTime", "")),
            priority=data.get("priority", ""),
            summary=data.get("summary", ""),
            suggested_action=data.get("suggested_action", data.get("action", "")),
            raw=data,
        )


class DraftReply(BaseModel):
    """Drafted email reply."""
    body_html: str = ""
    raw: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> DraftReply:
        return cls(
            body_html=data.get("body_html", data.get("draft", "")),
            raw=data,
        )


class ThreadMessage(BaseModel):
    """A single message inside an email thread."""
    id: str = ""
    sender: str = ""
    body: str = ""
    received_at: str = ""
    raw: dict[str, Any] = Field(default_factory=dict)


class EmailThread(BaseModel):
    """Full email thread/conversation."""
    conversation_id: str = ""
    subject: str = ""
    messages: list[ThreadMessage] = Field(default_factory=list)
    raw: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> EmailThread:
        msgs_raw = data.get("messages", [])
        msgs = [
            ThreadMessage(
                id=m.get("id", ""),
                sender=m.get("sender", m.get("from", "")),
                body=m.get("body", ""),
                received_at=m.get("received_at", m.get("receivedDateTime", "")),
                raw=m,
            )
            for m in msgs_raw
        ]
        return cls(
            conversation_id=data.get("conversation_id", data.get("id", "")),
            subject=data.get("subject", ""),
            messages=msgs,
            raw=data,
        )


# ── Delegations ──────────────────────────────────────────────────────

class Delegation(BaseModel):
    """A delegated item."""
    id: str = ""
    description: str = ""
    delegated_to: str = ""
    status: str = ""
    created_at: str = ""
    due_date: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Delegation:
        return cls(
            id=data.get("id", ""),
            description=data.get("description", data.get("title", "")),
            delegated_to=data.get("delegated_to", data.get("assignee", "")),
            status=data.get("status", ""),
            created_at=data.get("created_at", ""),
            due_date=data.get("due_date"),
            raw=data,
        )


# ── Knowledge Graph ──────────────────────────────────────────────────

class GraphNode(BaseModel):
    """A node in the knowledge graph."""
    id: str = ""
    label: str = ""
    type: str = ""
    properties: dict[str, Any] = Field(default_factory=dict)
    raw: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> GraphNode:
        return cls(
            id=data.get("id", ""),
            label=data.get("label", data.get("name", "")),
            type=data.get("type", data.get("node_type", "")),
            properties=data.get("properties", {}),
            raw=data,
        )


class GraphEdge(BaseModel):
    """A relationship/edge in the knowledge graph."""
    source: str = ""
    target: str = ""
    relationship: str = ""
    properties: dict[str, Any] = Field(default_factory=dict)
    raw: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> GraphEdge:
        return cls(
            source=data.get("source", data.get("from", "")),
            target=data.get("target", data.get("to", "")),
            relationship=data.get("relationship", data.get("type", "")),
            properties=data.get("properties", {}),
            raw=data,
        )


class GraphData(BaseModel):
    """Full graph response with nodes and edges."""
    nodes: list[GraphNode] = Field(default_factory=list)
    edges: list[GraphEdge] = Field(default_factory=list)
    raw: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> GraphData:
        nodes_raw = data.get("nodes", [])
        edges_raw = data.get("edges", data.get("relationships", []))
        return cls(
            nodes=[GraphNode.from_api(n) for n in nodes_raw],
            edges=[GraphEdge.from_api(e) for e in edges_raw],
            raw=data,
        )


# ── Tasks ────────────────────────────────────────────────────────────

class Task(BaseModel):
    """A task item."""
    id: str = ""
    description: str = ""
    assignee: str | None = None
    project: str | None = None
    status: str = ""
    created_at: str = ""
    raw: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Task:
        return cls(
            id=data.get("id", ""),
            description=data.get("description", data.get("title", "")),
            assignee=data.get("assignee"),
            project=data.get("project"),
            status=data.get("status", ""),
            created_at=data.get("created_at", ""),
            raw=data,
        )


# ── RPM (Results / Purpose / Massive Action Plan) ────────────────────

class RPMProject(BaseModel):
    """An RPM project."""
    id: str = ""
    result: str = ""
    purpose: str = ""
    massive_action_plan: list[str] = Field(default_factory=list)
    status: str = ""
    priority: int = 0
    due_date: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> RPMProject:
        return cls(
            id=data.get("id", ""),
            result=data.get("result", ""),
            purpose=data.get("purpose", ""),
            massive_action_plan=data.get("massive_action_plan", []),
            status=data.get("status", ""),
            priority=data.get("priority", 0),
            due_date=data.get("due_date"),
            raw=data,
        )


# ── Operations ───────────────────────────────────────────────────────

class Operation(BaseModel):
    """A recurring or one-off operation."""
    id: str = ""
    title: str = ""
    description: str = ""
    category: str = ""
    status: str = ""
    due_date: str | None = None
    recurrence: str = ""
    raw: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Operation:
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            category=data.get("category", ""),
            status=data.get("status", ""),
            due_date=data.get("due_date"),
            recurrence=data.get("recurrence", ""),
            raw=data,
        )


# ── Decisions ────────────────────────────────────────────────────────

class Decision(BaseModel):
    """A logged decision."""
    id: str = ""
    title: str = ""
    context: str = ""
    rationale: str = ""
    outcome: str | None = None
    created_at: str = ""
    raw: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Decision:
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            context=data.get("context", ""),
            rationale=data.get("rationale", ""),
            outcome=data.get("outcome"),
            created_at=data.get("created_at", ""),
            raw=data,
        )


# ── Capture / Inbox ─────────────────────────────────────────────────

class CaptureEvent(BaseModel):
    """A captured input event."""
    id: str = ""
    content: str = ""
    source: str = ""
    sender: str | None = None
    status: str = ""
    raw: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> CaptureEvent:
        return cls(
            id=data.get("id", ""),
            content=data.get("content", ""),
            source=data.get("source", ""),
            sender=data.get("sender"),
            status=data.get("status", ""),
            raw=data,
        )


# ── Someday / Maybe ─────────────────────────────────────────────────

class SomedayItem(BaseModel):
    """A someday/maybe list item."""
    id: str = ""
    title: str = ""
    description: str = ""
    area: str = ""
    raw: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> SomedayItem:
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            area=data.get("area", ""),
            raw=data,
        )


# ── Admin ────────────────────────────────────────────────────────────

class User(BaseModel):
    """A PILOT user."""
    id: str = ""
    email: str = ""
    name: str = ""
    plan: str = ""
    is_active: bool = True
    raw: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> User:
        return cls(
            id=data.get("id", ""),
            email=data.get("email", ""),
            name=data.get("name", data.get("display_name", "")),
            plan=data.get("plan", ""),
            is_active=data.get("is_active", True),
            raw=data,
        )


class Invite(BaseModel):
    """An invitation record."""
    id: str = ""
    code: str = ""
    email: str | None = None
    note: str | None = None
    created_at: str = ""
    raw: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Invite:
        return cls(
            id=data.get("id", ""),
            code=data.get("code", ""),
            email=data.get("email"),
            note=data.get("note"),
            created_at=data.get("created_at", ""),
            raw=data,
        )


class Stats(BaseModel):
    """Admin dashboard stats."""
    raw: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Stats:
        return cls(raw=data)


# ── API Keys ─────────────────────────────────────────────────────────

class APIKey(BaseModel):
    """An API key."""
    id: str = ""
    name: str = ""
    key: str = ""
    key_preview: str = ""
    last_used_at: str | None = None
    created_at: str = ""
    raw: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> APIKey:
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            key=data.get("key", ""),
            key_preview=data.get("key_preview", ""),
            last_used_at=data.get("last_used_at"),
            created_at=data.get("created_at", ""),
            raw=data,
        )
