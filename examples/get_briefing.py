"""Get your morning briefing and weekly review from PILOT."""

import os

from pilot import PilotClient

api_key = os.environ["PILOT_API_KEY"]

with PilotClient(api_key=api_key) as client:
    # Morning briefing
    briefing = client.briefing.get()
    print("=== Morning Briefing ===")
    print(briefing.summary)
    print()

    for item in briefing.focus_items:
        print(f"  [{item.priority}] {item.title}")
        if item.detail:
            print(f"        {item.detail}")

    # Force a fresh briefing (skip cache)
    fresh = client.briefing.get(refresh=True)
    print("\n=== Fresh Briefing ===")
    print(fresh.summary)

    # Weekly review
    review = client.briefing.get_weekly_review()
    print("\n=== Weekly Review ===")
    print(review.review)
