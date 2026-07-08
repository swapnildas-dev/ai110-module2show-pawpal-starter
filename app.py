import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+** — a pet care planning assistant. Add your pets and their care
tasks below, then generate today's schedule based on priority and your available time.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** helps a pet owner plan care tasks for their pet(s) based on constraints
like available time and task priority. Add pets, give them tasks, and generate a
schedule that fits the highest-priority tasks into the time you have today.
"""
    )

# --- Initialize the Owner in session state so pets/tasks persist across reruns ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_time=60)

owner = st.session_state.owner

st.divider()

st.subheader("Owner")
col1, col2 = st.columns(2)
with col1:
    owner.name = st.text_input("Owner name", value=owner.name)
with col2:
    owner.available_time = st.number_input(
        "Available time today (minutes)", min_value=0, max_value=600, value=owner.available_time
    )

st.divider()

st.subheader("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=40, value=1)
    submitted_pet = st.form_submit_button("Add pet")

if submitted_pet:
    if pet_name.strip():
        owner.add_pet(Pet(name=pet_name.strip(), species=species, age=int(age)))
        st.success(f"Added {pet_name}!")
    else:
        st.warning("Please enter a pet name.")

st.divider()

st.subheader("Your Pets")
if not owner.get_pets():
    st.info("No pets yet. Add one above.")
else:
    for pet in owner.get_pets():
        with st.expander(f"🐾 {pet.name} ({pet.species}, age {pet.age})", expanded=True):
            if pet.get_tasks():
                st.table(
                    [
                        {
                            "Task": task.name,
                            "Time": task.time or "-",
                            "Duration (min)": task.duration,
                            "Priority": task.priority,
                            "Repeats": task.recurrence or "-",
                            "Completed": task.completed,
                        }
                        for task in pet.get_tasks()
                    ]
                )
            else:
                st.caption("No tasks yet for this pet.")

st.divider()

st.subheader("Add a Task")
if not owner.get_pets():
    st.info("Add a pet first before adding tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        pet_names = [pet.name for pet in owner.get_pets()]
        selected_pet_name = st.selectbox("Which pet is this task for?", pet_names)
        task_title = st.text_input("Task title", value="Morning walk")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        time_str = st.text_input("Time (24-hour HH:MM, optional)", value="")
        st.caption("Set a time to enable time-based sorting and conflict checking, e.g. 07:30.")
        recurrence = st.selectbox("Repeats", ["none", "daily", "weekly"])
        submitted_task = st.form_submit_button("Add task")

    if submitted_task:
        selected_pet = next(pet for pet in owner.get_pets() if pet.name == selected_pet_name)
        selected_pet.add_task(
            Task(
                name=task_title,
                duration=int(duration),
                priority=priority,
                time=time_str.strip() or None,
                recurrence=None if recurrence == "none" else recurrence,
            )
        )
        st.success(f"Added '{task_title}' for {selected_pet_name}!")

st.divider()

st.subheader("Mark a Task Complete")
pets_with_tasks = [pet for pet in owner.get_pets() if pet.get_tasks()]
if not pets_with_tasks:
    st.info("Add a pet and a task first.")
else:
    complete_pet_name = st.selectbox(
        "Pet", [pet.name for pet in pets_with_tasks], key="complete_pet_select"
    )
    complete_pet = next(pet for pet in pets_with_tasks if pet.name == complete_pet_name)
    incomplete_tasks = [task for task in complete_pet.get_tasks() if not task.completed]

    if not incomplete_tasks:
        st.info(f"All of {complete_pet_name}'s tasks are already complete.")
    else:
        complete_task_name = st.selectbox(
            "Task", [task.name for task in incomplete_tasks], key="complete_task_select"
        )
        if st.button("Mark complete"):
            task_to_complete = next(
                task for task in incomplete_tasks if task.name == complete_task_name
            )
            recurrence = task_to_complete.recurrence
            next_task = task_to_complete.mark_complete()
            if next_task is not None:
                st.success(
                    f"Marked '{complete_task_name}' complete. Since it repeats {recurrence}, "
                    f"a new task was automatically scheduled for {next_task.date}."
                )
            else:
                st.success(f"Marked '{complete_task_name}' complete.")

st.divider()

st.subheader("Build Schedule")
st.caption(
    "Generates today's schedule from today's incomplete tasks, fitted to priority and available time."
)

if st.button("Generate schedule"):
    scheduler = Scheduler(owner=owner)
    scheduler.generate_schedule()
    scheduler.display_schedule()  # also prints to the terminal running streamlit
    st.session_state.last_schedule = scheduler.schedule

if "last_schedule" in st.session_state:
    st.markdown("### Today's Schedule")
    schedule = st.session_state.last_schedule

    sort_col1, sort_col2 = st.columns(2)
    with sort_col1:
        if st.button("Sort by priority"):
            temp_scheduler = Scheduler(owner=owner, schedule=schedule)
            temp_scheduler.sort_tasks()
            st.session_state.last_schedule = temp_scheduler.schedule
            schedule = st.session_state.last_schedule
    with sort_col2:
        if st.button("Sort by time"):
            temp_scheduler = Scheduler(owner=owner, schedule=schedule)
            temp_scheduler.sort_by_time()
            st.session_state.last_schedule = temp_scheduler.schedule
            schedule = st.session_state.last_schedule

    if schedule:
        st.table(
            [
                {
                    "Priority": task.priority.upper(),
                    "Time": task.time or "-",
                    "Task": task.name,
                    "Pet": task.pet_name or "-",
                    "Duration (min)": task.duration,
                }
                for task in schedule
            ]
        )
    else:
        st.info("No tasks fit in the available time. Add pets/tasks above and try again.")

st.divider()

st.subheader("Filter Tasks")
st.caption("Looks across every pet's full task list, not just today's schedule.")
if not owner.get_pets():
    st.info("Add a pet first to filter tasks.")
else:
    filter_scheduler = Scheduler(owner=owner)
    filter_pet_name = st.selectbox(
        "Filter by pet", ["All"] + [pet.name for pet in owner.get_pets()]
    )
    filter_status = st.radio("Filter by completion status", ["All", "Completed", "Incomplete"], horizontal=True)

    filtered_tasks = filter_scheduler.get_all_tasks()
    if filter_pet_name != "All":
        pet_matches = filter_scheduler.filter_by_pet(filter_pet_name)
        filtered_tasks = [task for task in filtered_tasks if task in pet_matches]
    if filter_status != "All":
        status_matches = filter_scheduler.filter_by_completion(filter_status == "Completed")
        filtered_tasks = [task for task in filtered_tasks if task in status_matches]

    if filtered_tasks:
        st.table(
            [
                {
                    "Task": task.name,
                    "Pet": task.pet_name or "-",
                    "Time": task.time or "-",
                    "Priority": task.priority,
                    "Completed": task.completed,
                }
                for task in filtered_tasks
            ]
        )
    else:
        st.info("No tasks match that filter.")

st.divider()

st.subheader("Conflict Check")
st.caption("Checks every pet's timed tasks for overlapping time slots on the same day.")
if st.button("Check for conflicts"):
    conflict_scheduler = Scheduler(owner=owner)
    conflicts = conflict_scheduler.find_conflicts()
    if conflicts:
        for task_a, task_b in conflicts:
            st.warning(
                f"Conflict on {task_a.date}: '{task_a.name}' ({task_a.time}) overlaps with "
                f"'{task_b.name}' ({task_b.time})"
            )
    else:
        st.success("No conflicts found.")
