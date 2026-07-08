"""Demo script for PawPal+: proves out sorting, filtering, recurrence, and conflict detection."""

from pawpal_system import Owner, Pet, Task, Scheduler


def print_tasks(label: str, tasks) -> None:
    """Print a labeled list of tasks in a compact, readable format."""
    print(label)
    if not tasks:
        print("  (none)")
    for task in tasks:
        time_str = task.time or "--:--"
        print(
            f"  [{task.priority.upper():6}] {task.name:20} pet={task.pet_name:6} "
            f"date={task.date} time={time_str} dur={task.duration:>3}min "
            f"completed={task.completed} recurrence={task.recurrence or 'none'}"
        )
    print()


def main() -> None:
    owner = Owner(name="Jordan", available_time=180)

    dog = Pet(name="Rex", species="dog", age=3)
    cat = Pet(name="Milo", species="cat", age=2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Tasks are added out of chronological order on purpose, to prove sort_by_time() works.
    dog.add_task(Task(name="Evening Walk", duration=30, priority="high", time="18:00"))
    dog.add_task(Task(name="Morning Walk", duration=30, priority="high", time="07:00"))
    dog.add_task(
        Task(name="Give Medication", duration=10, priority="high", time="07:15", recurrence="daily")
    )
    cat.add_task(Task(name="Feed Cat", duration=10, priority="high", time="08:00"))
    cat.add_task(
        Task(name="Vet Checkup", duration=45, priority="medium", time="09:00", recurrence="weekly")
    )
    # Deliberately overlaps with "Feed Cat" (08:00-08:10) to demonstrate conflict detection.
    cat.add_task(Task(name="Clean Litter Box", duration=20, priority="medium", time="08:05"))

    scheduler = Scheduler(owner=owner)

    print("=== 1. Tasks Added Out of Chronological Order ===")
    print_tasks("All tasks (in the order they were added):", scheduler.get_all_tasks())

    print("=== 2. Sorting by Time ===")
    scheduler.generate_schedule()
    scheduler.sort_by_time()
    print_tasks("Schedule sorted by time:", scheduler.schedule)

    print("=== 3. Filtering by Pet ===")
    print_tasks("Tasks for Rex:", scheduler.filter_by_pet("Rex"))
    print_tasks("Tasks for Milo:", scheduler.filter_by_pet("Milo"))

    print("=== 4. Filtering by Completion Status ===")
    dog.get_tasks()[0].mark_complete()  # Evening Walk: a one-time task, not recurring
    print_tasks("Completed tasks:", scheduler.filter_by_completion(True))
    print_tasks("Incomplete tasks:", scheduler.filter_by_completion(False))

    print("=== 5. Recurring Task Behavior ===")
    medication = next(task for task in dog.get_tasks() if task.name == "Give Medication")
    print(f"Completing '{medication.name}' (daily) scheduled for {medication.date}...")
    next_medication = medication.mark_complete()
    print(f"  -> Next occurrence automatically created for {next_medication.date}")
    print_tasks("Rex's tasks after completing the daily task:", dog.get_tasks())

    vet_checkup = next(task for task in cat.get_tasks() if task.name == "Vet Checkup")
    print(f"Completing '{vet_checkup.name}' (weekly) scheduled for {vet_checkup.date}...")
    next_vet_checkup = vet_checkup.mark_complete()
    print(f"  -> Next occurrence automatically created for {next_vet_checkup.date}")
    print_tasks("Milo's tasks after completing the weekly task:", cat.get_tasks())

    print("=== 6. Conflict Detection ===")
    conflicts = scheduler.find_conflicts()
    if conflicts:
        for task_a, task_b in conflicts:
            print(
                f"  CONFLICT on {task_a.date}: '{task_a.name}' ({task_a.time}) overlaps "
                f"with '{task_b.name}' ({task_b.time})"
            )
    else:
        print("  No conflicts found.")
    print()

    print("=== Final Schedule ===")
    scheduler.generate_schedule()
    scheduler.display_schedule()


if __name__ == "__main__":
    main()
