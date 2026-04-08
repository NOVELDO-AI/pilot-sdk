"""Tasks resource — task management."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pilot.models import Task

if TYPE_CHECKING:
    from pilot.client import PilotClient


class TasksResource:
    """Create and manage tasks."""

    def __init__(self, client: PilotClient) -> None:
        self._client = client

    def list(self) -> list[Task]:
        """List all tasks.

        Returns:
            List of Task objects.
        """
        data = self._client._request("GET", "/api/v1/tasks")
        items = data if isinstance(data, list) else data.get("tasks", data.get("items", []))
        return [Task.from_api(t) for t in items]

    def create(
        self,
        description: str,
        *,
        assignee: str | None = None,
        project: str | None = None,
    ) -> Task:
        """Create a new task.

        Args:
            description: What needs to be done.
            assignee: Who should do it (optional).
            project: Which project it belongs to (optional).

        Returns:
            The created Task.
        """
        payload: dict[str, Any] = {"description": description}
        if assignee is not None:
            payload["assignee"] = assignee
        if project is not None:
            payload["project"] = project
        data = self._client._request("POST", "/api/v1/tasks", json=payload)
        return Task.from_api(data)

    def complete(self, task_id: str) -> dict[str, Any]:
        """Mark a task as complete.

        Args:
            task_id: The task ID.

        Returns:
            Raw API response dict.
        """
        return self._client._request("POST", f"/api/v1/tasks/{task_id}/complete")

    def reopen(self, task_id: str) -> dict[str, Any]:
        """Reopen a completed task.

        Args:
            task_id: The task ID.

        Returns:
            Raw API response dict.
        """
        return self._client._request("POST", f"/api/v1/tasks/{task_id}/reopen")
