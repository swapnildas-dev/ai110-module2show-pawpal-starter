"""Basic tests for the PawPal+ core classes."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pawpal_system import Pet, Task


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
