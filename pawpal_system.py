"""Class scaffolding for PawPal+, generated from diagrams/uml.mmd."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    name: str
    duration: int
    priority: str
    completed: bool = False

    def mark_complete(self) -> None:
        pass

    def update_priority(self, priority: str) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task_name: str) -> None:
        pass

    def get_tasks(self) -> List[Task]:
        pass


class Owner:
    def __init__(self, name: str, available_time: int, pets: List[Pet] = None):
        self.name = name
        self.available_time = available_time
        self.pets = pets if pets is not None else []

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet_name: str) -> None:
        pass

    def get_pets(self) -> List[Pet]:
        pass


class Scheduler:
    def __init__(self, owner: Owner, schedule: List[Task] = None):
        self.owner = owner
        self.schedule = schedule if schedule is not None else []

    def generate_schedule(self) -> None:
        pass

    def sort_tasks(self) -> None:
        pass

    def display_schedule(self) -> None:
        pass
