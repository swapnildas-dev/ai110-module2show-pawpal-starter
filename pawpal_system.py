"""Class scaffolding for PawPal+, generated from diagrams/uml.mmd."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Tuple


@dataclass
class Task:
    name: str
    duration: int
    priority: str
    completed: bool = False
    pet_name: Optional[str] = None
    date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    time: Optional[str] = None
    recurrence: Optional[str] = None
    # Set automatically by Pet.add_task() so mark_complete() can re-attach recurring tasks.
    _pet: Optional["Pet"] = field(default=None, repr=False, compare=False)

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task complete and, if it recurs, create (and attach) the next occurrence."""
        self.completed = True

        if self.recurrence not in ("daily", "weekly"):
            return None

        current_date = datetime.strptime(self.date, "%Y-%m-%d")
        step = timedelta(days=1) if self.recurrence == "daily" else timedelta(weeks=1)
        next_date = (current_date + step).strftime("%Y-%m-%d")

        next_task = Task(
            name=self.name,
            duration=self.duration,
            priority=self.priority,
            completed=False,
            pet_name=self.pet_name,
            date=next_date,
            time=self.time,
            recurrence=self.recurrence,
        )

        if self._pet is not None:
            self._pet.add_task(next_task)

        return next_task

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
        task._pet = self
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

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all of the owner's pets, regardless of date or status."""
        return [task for pet in self.owner.get_pets() for task in pet.get_tasks()]

    def generate_schedule(self) -> None:
        """Build today's schedule from today's incomplete tasks that fit in the owner's available time."""
        today = datetime.now().strftime("%Y-%m-%d")
        todays_tasks = [
            task for task in self.get_all_tasks() if not task.completed and task.date == today
        ]

        self.schedule = todays_tasks
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

    def sort_by_time(self) -> None:
        """Sort the current schedule chronologically by each task's HH:MM time."""
        self.schedule = sorted(
            self.schedule, key=lambda task: (task.time is None, task.time or "")
        )

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return every task belonging to the given pet, across all pets' task lists."""
        return [task for task in self.get_all_tasks() if task.pet_name == pet_name]

    def filter_by_completion(self, completed: bool) -> List[Task]:
        """Return every task whose completed status matches the given value."""
        return [task for task in self.get_all_tasks() if task.completed == completed]

    def find_conflicts(self) -> List[Tuple[Task, Task]]:
        """Return pairs of timed tasks on the same date whose time ranges overlap."""
        timed_tasks = [task for task in self.get_all_tasks() if task.time is not None]

        conflicts = []
        for i in range(len(timed_tasks)):
            for j in range(i + 1, len(timed_tasks)):
                task_a, task_b = timed_tasks[i], timed_tasks[j]
                if task_a.date == task_b.date and self._times_overlap(task_a, task_b):
                    conflicts.append((task_a, task_b))

        return conflicts

    @staticmethod
    def _times_overlap(task_a: Task, task_b: Task) -> bool:
        """Check whether two tasks' HH:MM time ranges overlap, given their durations."""
        start_a = datetime.strptime(task_a.time, "%H:%M")
        end_a = start_a + timedelta(minutes=task_a.duration)
        start_b = datetime.strptime(task_b.time, "%H:%M")
        end_b = start_b + timedelta(minutes=task_b.duration)
        return start_a < end_b and start_b < end_a

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
