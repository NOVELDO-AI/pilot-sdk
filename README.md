# pilot-sdk

Python SDK for [PILOT](https://withpilot.ai) — AI Chief of Staff API.

## Installation

```bash
pip install pilot-sdk
```

## Quick Start

```python
from pilot import PilotClient

client = PilotClient(api_key="pk_live_...")

# Morning briefing
briefing = client.briefing.get()
print(briefing.summary)

# Chat
reply = client.chat.send("What should I focus on today?")
print(reply)

# Email triage
emails = client.email.triage(limit=10)
for email in emails:
    print(f"{email.sender}: {email.subject} [{email.priority}]")

# Tasks
tasks = client.tasks.list()
client.tasks.create("Review Q2 numbers", assignee="Ren")
```

## Authentication

The SDK accepts both API keys and JWT tokens:

```python
# API key
client = PilotClient(api_key="pk_live_abc123")

# JWT token
client = PilotClient(api_key="eyJhbGciOiJIUzI1NiIs...")
```

Generate API keys in the PILOT dashboard under Settings > API Keys.

## Resources

| Resource | Description |
|---|---|
| `client.briefing` | Morning briefing, weekly review |
| `client.chat` | Conversational interaction (with history) |
| `client.email` | Triage, draft/send replies, batch operations |
| `client.tasks` | Create, complete, reopen tasks |
| `client.delegations` | Track delegated items |
| `client.decisions` | Log and search decisions |
| `client.rpm` | RPM projects (Results / Purpose / Massive Action Plan) |
| `client.operations` | Recurring and one-off operations |
| `client.graph` | Knowledge graph: nodes, edges, search |
| `client.capture` | Raw input capture and inbox |
| `client.someday` | Someday/maybe list |
| `client.admin` | Users, invites, stats, settings |

## Examples

### Email Workflow

```python
# Triage and auto-archive low priority
emails = client.email.triage(limit=30)
low = [e.id for e in emails if e.priority == "low"]
if low:
    client.email.batch_archive(low)

# Draft and send a reply
draft = client.email.draft_reply(message_id, tone="brief")
client.email.send_reply(message_id, draft.body_html)
```

### Knowledge Graph

```python
# Search the graph
results = client.graph.search("askSOPia pricing")
for node in results:
    print(f"{node.type}: {node.label}")

# Get full graph
graph = client.graph.get()
print(f"{len(graph.nodes)} nodes, {len(graph.edges)} edges")
```

### RPM Projects

```python
project = client.rpm.create(
    result="Launch askSOPia pilot program",
    purpose="Validate PMF with 3 paying customers",
    massive_action_plan=[
        "Run direct mail campaign",
        "Book 10 demo calls/week",
        "Deliver first Knowledge Transfer Sprint",
    ],
)
```

### Multi-turn Chat

```python
client.chat.send("What's on my plate today?")
client.chat.send("Tell me more about the first item.")
client.chat.send("Delegate that to Patrick.")
client.chat.clear_history()  # reset conversation
```

## Configuration

```python
client = PilotClient(
    api_key="pk_live_...",
    base_url="https://app.withpilot.ai",  # default
    timeout=30.0,                          # seconds
    headers={"X-Custom": "value"},         # extra headers
)
```

Use as a context manager to auto-close:

```python
with PilotClient(api_key="pk_live_...") as client:
    briefing = client.briefing.get()
```

## Error Handling

```python
from pilot import PilotClient, AuthenticationError, NotFoundError, RateLimitError

try:
    client.tasks.complete("nonexistent-id")
except NotFoundError:
    print("Task not found")
except AuthenticationError:
    print("Bad API key")
except RateLimitError:
    print("Slow down")
```

All exceptions inherit from `PilotError` and include `status_code` and `body` attributes.

## Development

```bash
git clone https://github.com/NOVELDO-AI/pilot-sdk.git
cd pilot-sdk
pip install -e ".[dev]"
```

## License

MIT
