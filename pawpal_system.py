"""Class scaffolding for PawPal+, generated from diagrams/uml.mmd."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    name: str
    duration: int
    priority: str
    completed: bool = False
    pet_name: Optional[str] = None

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def update_priority(self, priority: str) -> None:
        """Update this task's priority level."""
        self.priority = priority


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list and tag it with the pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task_name: str) -> None:
        """Remove a task from this pet's task list by name."""
        self.tasks = [task for task in self.tasks if task.name != task_name]

    def get_tasks(self) -> List[Task]:
        """Return this pet's list of tasks."""
        return self.tasks


class Owner:
    def __init__(self, name: str, available_time: int, pets: Optional[List[Pet]] = None):
        """Create an owner with a name, available time, and an optional list of pets."""
        self.name = name
        self.available_time = available_time
        self.pets = pets if pets is not None else []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet from this owner's list by name."""
        self.pets = [pet for pet in self.pets if pet.name != pet_name]

    def get_pets(self) -> List[Pet]:
        """Return this owner's list of pets."""
        return self.pets


class Scheduler:
    # High-priority tasks come first, then medium, then low.
    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    def __init__(self, owner: Owner, schedule: Optional[List[Task]] = None):
        """Create a scheduler for an owner with an optional starting schedule."""
        self.owner = owner
        self.schedule = schedule if schedule is not None else []

    def generate_schedule(self) -> None:
        """Build today's schedule from all pets' tasks that fit in the owner's available time."""
        all_tasks = [
            task
            for pet in self.owner.get_pets()
            for task in pet.get_tasks()
            if not task.completed
        ]

        self.schedule = all_tasks
        self.sort_tasks()

        fitted_tasks = []
        remaining_time = self.owner.available_time
        for task in self.schedule:
            if task.duration <= remaining_time:
                fitted_tasks.append(task)
                remaining_time -= task.duration

        self.schedule = fitted_tasks

    def sort_tasks(self) -> None:
        """Sort the current schedule by priority: high first, then medium, then low."""
        self.schedule.sort(
            key=lambda task: self.PRIORITY_ORDER.get(task.priority.lower(), len(self.PRIORITY_ORDER))
        )

    def display_schedule(self) -> None:
        """Print today's schedule in a clean, readable format."""
        print("Today's Schedule")
        print("-----------------")

        if not self.schedule:
            print("No tasks scheduled.")
            return

        for task in self.schedule:
            pet_info = f" ({task.pet_name})" if task.pet_name else ""
            print(f"[{task.priority.upper()}] {task.name}{pet_info} - {task.duration} min")
