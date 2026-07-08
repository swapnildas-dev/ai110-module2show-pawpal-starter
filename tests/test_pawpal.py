"""Basic tests for the PawPal+ core classes."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_complete_changes_status():
    task = Task(name="Feed", duration=10, priority="high")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Rex", species="dog", age=3)
    assert len(pet.get_tasks()) == 0

    pet.add_task(Task(name="Walk", duration=20, priority="medium"))

    assert len(pet.get_tasks()) == 1


def test_sort_by_time_orders_tasks_chronologically():
    owner = Owner(name="Jordan", available_time=120)
    pet = Pet(name="Rex", species="dog", age=3)
    owner.add_pet(pet)
    pet.add_task(Task(name="Evening", duration=10, priority="low", time="18:00"))
    pet.add_task(Task(name="Morning", duration=10, priority="low", time="07:00"))

    scheduler = Scheduler(owner=owner)
    scheduler.schedule = pet.get_tasks()
    scheduler.sort_by_time()

    assert [task.name for task in scheduler.schedule] == ["Morning", "Evening"]


def test_filter_by_pet_returns_only_that_pets_tasks():
    owner = Owner(name="Jordan", available_time=120)
    rex = Pet(name="Rex", species="dog", age=3)
    milo = Pet(name="Milo", species="cat", age=2)
    owner.add_pet(rex)
    owner.add_pet(milo)
    rex.add_task(Task(name="Walk", duration=20, priority="high"))
    milo.add_task(Task(name="Feed", duration=10, priority="high"))

    scheduler = Scheduler(owner=owner)

    assert [task.name for task in scheduler.filter_by_pet("Rex")] == ["Walk"]


def test_filter_by_completion_returns_matching_tasks():
    owner = Owner(name="Jordan", available_time=120)
    pet = Pet(name="Rex", species="dog", age=3)
    owner.add_pet(pet)
    done_task = Task(name="Walk", duration=20, priority="high")
    pending_task = Task(name="Feed", duration=10, priority="high")
    pet.add_task(done_task)
    pet.add_task(pending_task)
    done_task.mark_complete()

    scheduler = Scheduler(owner=owner)

    assert [task.name for task in scheduler.filter_by_completion(True)] == ["Walk"]
    assert [task.name for task in scheduler.filter_by_completion(False)] == ["Feed"]


def test_daily_recurring_task_creates_next_day_task():
    owner = Owner(name="Jordan", available_time=120)
    pet = Pet(name="Rex", species="dog", age=3)
    owner.add_pet(pet)
    task = Task(
        name="Medication", duration=5, priority="high", date="2026-01-01", recurrence="daily"
    )
    pet.add_task(task)

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.date == "2026-01-02"
    assert next_task.completed is False
    assert next_task in pet.get_tasks()


def test_weekly_recurring_task_creates_next_week_task():
    owner = Owner(name="Jordan", available_time=120)
    pet = Pet(name="Milo", species="cat", age=2)
    owner.add_pet(pet)
    task = Task(
        name="Vet Checkup", duration=45, priority="medium", date="2026-01-01", recurrence="weekly"
    )
    pet.add_task(task)

    next_task = task.mark_complete()

    assert next_task.date == "2026-01-08"


def test_find_conflicts_detects_overlapping_times():
    owner = Owner(name="Jordan", available_time=120)
    pet = Pet(name="Rex", species="dog", age=3)
    owner.add_pet(pet)
    pet.add_task(Task(name="Walk", duration=30, priority="high", time="08:00", date="2026-01-01"))
    pet.add_task(Task(name="Feed", duration=15, priority="high", time="08:15", date="2026-01-01"))

    scheduler = Scheduler(owner=owner)
    conflicts = scheduler.find_conflicts()

    assert len(conflicts) == 1
    names = {conflicts[0][0].name, conflicts[0][1].name}
    assert names == {"Walk", "Feed"}
