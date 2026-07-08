"""Demo script for PawPal+: builds an owner, some pets and tasks, and prints today's schedule."""

from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner(name="Jordan", available_time=60)

    dog = Pet(name="Rex", species="dog", age=3)
    cat = Pet(name="Milo", species="cat", age=2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task(name="Morning Walk", duration=30, priority="high"))
    dog.add_task(Task(name="Brush Fur", duration=15, priority="low"))
    cat.add_task(Task(name="Feed Cat", duration=10, priority="high"))
    cat.add_task(Task(name="Clean Litter Box", duration=20, priority="medium"))

    scheduler = Scheduler(owner=owner)
    scheduler.generate_schedule()
    scheduler.display_schedule()


if __name__ == "__main__":
    main()
