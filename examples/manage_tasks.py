"""Task and RPM project management examples."""

import os

from pilot import PilotClient

api_key = os.environ["PILOT_API_KEY"]

with PilotClient(api_key=api_key) as client:
    # --- Tasks ---
    print("=== Tasks ===")
    tasks = client.tasks.list()
    for task in tasks:
        status = "x" if task.status == "done" else " "
        print(f"  [{status}] {task.description} (assignee: {task.assignee or 'me'})")

    # Create a task
    new_task = client.tasks.create(
        "Review Q2 pipeline numbers",
        assignee="Ren",
        project="askSOPia Sales",
    )
    print(f"\nCreated task: {new_task.description} (id: {new_task.id})")

    # Complete a task
    if tasks:
        client.tasks.complete(tasks[0].id)
        print(f"Completed: {tasks[0].description}")

    # --- RPM Projects ---
    print("\n=== RPM Projects ===")
    projects = client.rpm.list(status="active")
    for p in projects:
        print(f"  Result: {p.result}")
        print(f"  Purpose: {p.purpose}")
        for step in p.massive_action_plan:
            print(f"    - {step}")
        print()

    # Create an RPM project
    rpm = client.rpm.create(
        result="Close 3 askSOPia pilot customers by end of Q2",
        purpose="Validate product-market fit and generate first revenue",
        massive_action_plan=[
            "Finalize direct mail campaign for 50 target firms",
            "Run 10 demo calls per week",
            "Deliver Knowledge Transfer Sprint to first customer",
        ],
        priority=1,
    )
    print(f"Created RPM project: {rpm.result} (id: {rpm.id})")

    # --- Delegations ---
    print("\n=== Waiting Delegations ===")
    delegations = client.delegations.list(status="waiting")
    for d in delegations:
        print(f"  {d.description} -> {d.delegated_to} ({d.status})")

    # --- Decisions ---
    print("\n=== Recent Decisions ===")
    decisions = client.decisions.list()
    for d in decisions[:5]:
        print(f"  {d.title}: {d.rationale[:80]}")

    # Log a decision
    decision = client.decisions.create(
        title="Switch from Replit to Vercel for askSOPia hosting",
        context="Replit deployment unreliable, cold starts too slow",
        rationale="Vercel has better Next.js support, faster builds, predictable pricing",
    )
    print(f"\nLogged decision: {decision.title}")
