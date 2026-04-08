"""Email triage workflow — review, draft, and manage email."""

import os

from pilot import PilotClient

api_key = os.environ["PILOT_API_KEY"]

with PilotClient(api_key=api_key) as client:
    # Get triaged emails
    emails = client.email.triage(limit=10)
    print(f"=== {len(emails)} Triaged Emails ===")

    archive_ids: list[str] = []

    for email in emails:
        print(f"\n  From: {email.sender}")
        print(f"  Subject: {email.subject}")
        print(f"  Priority: {email.priority}")
        print(f"  Action: {email.suggested_action}")

        # Auto-archive low priority
        if email.priority == "low":
            archive_ids.append(email.id)

    # Batch archive low-priority emails
    if archive_ids:
        client.email.batch_archive(archive_ids)
        print(f"\nArchived {len(archive_ids)} low-priority emails.")

    # Draft a reply to the first high-priority email
    high_priority = [e for e in emails if e.priority == "high"]
    if high_priority:
        draft = client.email.draft_reply(high_priority[0].id, tone="professional")
        print(f"\n=== Draft Reply ===")
        print(draft.body_html[:200])

    # Check unanswered emails from last 5 days
    unanswered = client.email.unanswered(days=5)
    print(f"\n{len(unanswered)} unanswered emails in the last 5 days.")
