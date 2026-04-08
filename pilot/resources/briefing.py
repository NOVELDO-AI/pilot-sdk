"""Briefing resource — morning briefing and weekly review."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pilot.models import Briefing, WeeklyReview

if TYPE_CHECKING:
    from pilot.client import PilotClient


class BriefingResource:
    """Access morning briefings and weekly reviews."""

    def __init__(self, client: PilotClient) -> None:
        self._client = client

    def get(self, *, refresh: bool = False) -> Briefing:
        """Fetch the morning briefing.

        Args:
            refresh: Force regeneration instead of returning cached version.

        Returns:
            Briefing with summary and focus items.
        """
        params: dict[str, str] = {}
        if refresh:
            params["refresh"] = "true"
        data = self._client._request("GET", "/api/v1/briefing", params=params)
        return Briefing.from_api(data)

    def get_weekly_review(self) -> WeeklyReview:
        """Fetch the weekly accountability review (cached for 1 hour).

        Returns:
            WeeklyReview with the review text.
        """
        data = self._client._request("GET", "/api/v1/weekly-review")
        return WeeklyReview.from_api(data)
