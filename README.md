# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting (priority) | `Scheduler.sort_tasks()` | Sorts by priority: high, then medium, then low. |
| Task sorting (time) | `Scheduler.sort_by_time()` | Uses `sorted()` with a lambda key on each task's `"HH:MM"` time string; tasks with no time are placed last. |
| Filtering | `Scheduler.filter_by_pet(pet_name)`, `Scheduler.filter_by_completion(completed)` | Filter across every pet's tasks by pet name or by completed/incomplete status. |
| Conflict handling | `Scheduler.find_conflicts()` | Compares every pair of timed tasks on the same date and flags any whose `time`–`time + duration` ranges overlap. |
| Recurring tasks | `Task.mark_complete()` | When a task with `recurrence="daily"` or `"weekly"` is marked complete, a new copy of it is automatically created (and attached to the same pet) dated one day or one week later, using `datetime`/`timedelta`. |

### How each piece works

- **Sorting by time**: `Task.time` is stored as an `"HH:MM"` string. `sort_by_time()` calls `sorted()` with `key=lambda task: (task.time is None, task.time or "")`, so zero-padded 24-hour strings compare correctly and undated tasks sort to the end.
- **Filtering**: both filter methods look across *all* of the owner's pets (not just today's fitted schedule), so you can find a pet's full task history or every completed/incomplete task regardless of date.
- **Conflict detection**: only tasks that have a `time` set are compared; two tasks conflict if they fall on the same `date` and their `[start, start + duration)` windows overlap.
- **Recurring tasks**: each `Task` has a `date` (defaults to today) and a `recurrence` (`"daily"`, `"weekly"`, or `None`). `Pet.add_task()` tags the task with a private back-reference to its pet, so when `mark_complete()` runs on a recurring task it can build the next occurrence and add it straight to that pet's task list automatically — no extra wiring needed by the caller.

See `main.py` for a runnable demo of every feature above, including intentionally out-of-order task creation, a live conflict, and a full daily/weekly recurrence cycle.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
