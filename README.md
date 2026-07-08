# PawPal+ (Module 2 Project)

**PawPal+** is a Streamlit app that helps a pet owner plan care tasks for their pet(s) —
add pets and tasks, generate a priority-based daily schedule, and catch scheduling
conflicts before they happen.

## ✨ Features

- **Owner & pet management** — set your name and available time for the day, add multiple pets, and see each pet's task list at a glance.
- **Task creation** — give each task a name, duration, priority, an optional time (`HH:MM`), and an optional recurrence (`daily` / `weekly`).
- **Smart scheduling** — `Scheduler.generate_schedule()` builds today's plan from incomplete, today-dated tasks, sorted by priority, fitted to however much time the owner has.
- **Sorting** — re-sort the generated schedule by priority or by time of day.
- **Filtering** — look across every pet's full task list by pet name and/or completion status.
- **Recurring tasks** — mark a daily or weekly task complete and PawPal+ automatically schedules the next occurrence for that pet.
- **Conflict detection** — flags any two timed tasks on the same day whose time ranges overlap.
- Everything persists in `st.session_state` for the length of the browser session, so pets/tasks stick around as you click through the app.

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

Running `python main.py` walks through every scheduler feature end-to-end. Real output
(dates shown are relative to whatever day you run it):

```
=== 1. Tasks Added Out of Chronological Order ===
All tasks (in the order they were added):
  [HIGH  ] Evening Walk         pet=Rex    date=2026-07-07 time=18:00 dur= 30min completed=False recurrence=none
  [HIGH  ] Morning Walk         pet=Rex    date=2026-07-07 time=07:00 dur= 30min completed=False recurrence=none
  [HIGH  ] Give Medication      pet=Rex    date=2026-07-07 time=07:15 dur= 10min completed=False recurrence=daily
  [HIGH  ] Feed Cat             pet=Milo   date=2026-07-07 time=08:00 dur= 10min completed=False recurrence=none
  [MEDIUM] Vet Checkup          pet=Milo   date=2026-07-07 time=09:00 dur= 45min completed=False recurrence=weekly
  [MEDIUM] Clean Litter Box     pet=Milo   date=2026-07-07 time=08:05 dur= 20min completed=False recurrence=none

=== 2. Sorting by Time ===
Schedule sorted by time:
  [HIGH  ] Morning Walk         pet=Rex    date=2026-07-07 time=07:00 dur= 30min completed=False recurrence=none
  [HIGH  ] Give Medication      pet=Rex    date=2026-07-07 time=07:15 dur= 10min completed=False recurrence=daily
  [HIGH  ] Feed Cat             pet=Milo   date=2026-07-07 time=08:00 dur= 10min completed=False recurrence=none
  [MEDIUM] Clean Litter Box     pet=Milo   date=2026-07-07 time=08:05 dur= 20min completed=False recurrence=none
  [MEDIUM] Vet Checkup          pet=Milo   date=2026-07-07 time=09:00 dur= 45min completed=False recurrence=weekly
  [HIGH  ] Evening Walk         pet=Rex    date=2026-07-07 time=18:00 dur= 30min completed=False recurrence=none

=== 3. Filtering by Pet ===
Tasks for Rex:
  [HIGH  ] Evening Walk         pet=Rex    date=2026-07-07 time=18:00 dur= 30min completed=False recurrence=none
  [HIGH  ] Morning Walk         pet=Rex    date=2026-07-07 time=07:00 dur= 30min completed=False recurrence=none
  [HIGH  ] Give Medication      pet=Rex    date=2026-07-07 time=07:15 dur= 10min completed=False recurrence=daily

Tasks for Milo:
  [HIGH  ] Feed Cat             pet=Milo   date=2026-07-07 time=08:00 dur= 10min completed=False recurrence=none
  [MEDIUM] Vet Checkup          pet=Milo   date=2026-07-07 time=09:00 dur= 45min completed=False recurrence=weekly
  [MEDIUM] Clean Litter Box     pet=Milo   date=2026-07-07 time=08:05 dur= 20min completed=False recurrence=none

=== 4. Filtering by Completion Status ===
Completed tasks:
  [HIGH  ] Evening Walk         pet=Rex    date=2026-07-07 time=18:00 dur= 30min completed=True recurrence=none

Incomplete tasks:
  [HIGH  ] Morning Walk         pet=Rex    date=2026-07-07 time=07:00 dur= 30min completed=False recurrence=none
  [HIGH  ] Give Medication      pet=Rex    date=2026-07-07 time=07:15 dur= 10min completed=False recurrence=daily
  [HIGH  ] Feed Cat             pet=Milo   date=2026-07-07 time=08:00 dur= 10min completed=False recurrence=none
  [MEDIUM] Vet Checkup          pet=Milo   date=2026-07-07 time=09:00 dur= 45min completed=False recurrence=weekly
  [MEDIUM] Clean Litter Box     pet=Milo   date=2026-07-07 time=08:05 dur= 20min completed=False recurrence=none

=== 5. Recurring Task Behavior ===
Completing 'Give Medication' (daily) scheduled for 2026-07-07...
  -> Next occurrence automatically created for 2026-07-08
Rex's tasks after completing the daily task:
  [HIGH  ] Evening Walk         pet=Rex    date=2026-07-07 time=18:00 dur= 30min completed=True recurrence=none
  [HIGH  ] Morning Walk         pet=Rex    date=2026-07-07 time=07:00 dur= 30min completed=False recurrence=none
  [HIGH  ] Give Medication      pet=Rex    date=2026-07-07 time=07:15 dur= 10min completed=True recurrence=daily
  [HIGH  ] Give Medication      pet=Rex    date=2026-07-08 time=07:15 dur= 10min completed=False recurrence=daily

Completing 'Vet Checkup' (weekly) scheduled for 2026-07-07...
  -> Next occurrence automatically created for 2026-07-14
Milo's tasks after completing the weekly task:
  [HIGH  ] Feed Cat             pet=Milo   date=2026-07-07 time=08:00 dur= 10min completed=False recurrence=none
  [MEDIUM] Vet Checkup          pet=Milo   date=2026-07-07 time=09:00 dur= 45min completed=True recurrence=weekly
  [MEDIUM] Clean Litter Box     pet=Milo   date=2026-07-07 time=08:05 dur= 20min completed=False recurrence=none
  [MEDIUM] Vet Checkup          pet=Milo   date=2026-07-14 time=09:00 dur= 45min completed=False recurrence=weekly

=== 6. Conflict Detection ===
  CONFLICT on 2026-07-07: 'Morning Walk' (07:00) overlaps with 'Give Medication' (07:15)
  CONFLICT on 2026-07-07: 'Feed Cat' (08:00) overlaps with 'Clean Litter Box' (08:05)

=== Final Schedule ===
Today's Schedule
-----------------
[HIGH] Morning Walk (Rex) - 30 min
[HIGH] Feed Cat (Milo) - 10 min
[MEDIUM] Clean Litter Box (Milo) - 20 min
```

## 🧪 Testing PawPal+

```bash
python -m pytest -v
```

The test suite (`tests/test_pawpal.py`, 13 tests) covers:

- **Core class behavior**: `Task.mark_complete()` flips `completed` to `True`, and `Pet.add_task()` increases that pet's task count.
- **Sorting correctness**: `Scheduler.sort_by_time()` returns tasks in chronological order (including a 3-task case and a case where an untimed task is correctly pushed to the end).
- **Filtering**: `Scheduler.filter_by_pet()` and `filter_by_completion()` return only the matching tasks.
- **Recurrence logic**: marking a `"daily"` task complete creates a new incomplete task dated exactly one day later, and a `"weekly"` task creates one dated a week later — both attached to the original pet.
- **Conflict detection**: `Scheduler.find_conflicts()` flags overlapping times and duplicate start times, and correctly reports *no* conflict for back-to-back tasks or tasks on different dates (negative cases, to catch false positives).
- **Editing tasks**: `Pet.remove_task()` removes only the named task and leaves the rest untouched.

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.13.9, pytest-8.4.2, pluggy-1.5.0
collected 13 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [  7%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 15%]
tests/test_pawpal.py::test_sort_by_time_orders_tasks_chronologically PASSED [ 23%]
tests/test_pawpal.py::test_sort_by_time_places_untimed_tasks_last PASSED [ 30%]
tests/test_pawpal.py::test_remove_task_removes_only_matching_task PASSED [ 38%]
tests/test_pawpal.py::test_filter_by_pet_returns_only_that_pets_tasks PASSED [ 46%]
tests/test_pawpal.py::test_filter_by_completion_returns_matching_tasks PASSED [ 53%]
tests/test_pawpal.py::test_daily_recurring_task_creates_next_day_task PASSED [ 61%]
tests/test_pawpal.py::test_weekly_recurring_task_creates_next_week_task PASSED [ 69%]
tests/test_pawpal.py::test_find_conflicts_detects_overlapping_times PASSED [ 76%]
tests/test_pawpal.py::test_find_conflicts_detects_duplicate_start_times PASSED [ 84%]
tests/test_pawpal.py::test_find_conflicts_ignores_back_to_back_tasks PASSED [ 92%]
tests/test_pawpal.py::test_find_conflicts_ignores_tasks_on_different_dates PASSED [100%]

============================== 13 passed in 0.02s ===============================
```

**Confidence: ⭐⭐⭐⭐☆ (4/5)** — every core scheduling behavior (sorting, filtering, recurrence, conflict detection) has both a positive and, where it matters, a negative test case, all passing. It's not a 5/5 because the suite only exercises `pawpal_system.py` directly; `app.py` (the Streamlit UI wiring) has no automated tests yet.

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

Run `streamlit run app.py` and follow along:

1. **Set the owner** — enter your name and how many minutes you have available today.
2. **Add a pet** — fill in the "Add a Pet" form (name, species, age) and submit. It shows up under "Your Pets."
3. **Add a task** — pick a pet, give the task a name, duration, and priority. Optionally set a time (`HH:MM`) and whether it repeats daily/weekly.
4. **Mark a task complete** — pick a pet and task under "Mark a Task Complete." If it repeats, PawPal+ tells you the next occurrence's date.
5. **Generate the schedule** — click "Generate schedule" to build today's plan from today's incomplete tasks, fitted to your available time and sorted by priority.
6. **Sort the schedule** — use "Sort by priority" or "Sort by time" to reorder the schedule that's currently on screen.
7. **Filter tasks** — use the pet and completion-status filters to see a specific pet's tasks or just what's done/not done, across all dates.
8. **Check for conflicts** — click "Check for conflicts" to see any overlapping timed tasks flagged as warnings (or a success message if there aren't any).

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
