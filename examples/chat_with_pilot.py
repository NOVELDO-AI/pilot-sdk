"""Chat with PILOT — multi-turn conversation example."""

import os

from pilot import PilotClient

api_key = os.environ["PILOT_API_KEY"]

with PilotClient(api_key=api_key) as client:
    # Simple one-shot question
    reply = client.chat.send("What should I focus on today?")
    print(f"PILOT: {reply}")
    print()

    # Multi-turn conversation (history is tracked automatically)
    reply = client.chat.send("Tell me more about the first item.")
    print(f"PILOT: {reply}")
    print()

    reply = client.chat.send("Schedule that for tomorrow morning.")
    print(f"PILOT: {reply}")
    print()

    # Start a fresh conversation
    client.chat.clear_history()
    reply = client.chat.send("What delegations are overdue?")
    print(f"PILOT: {reply}")
