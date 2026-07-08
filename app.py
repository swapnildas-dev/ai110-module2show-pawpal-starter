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
                            "Duration (min)": task.duration,
                            "Priority": task.priority,
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
        submitted_task = st.form_submit_button("Add task")

    if submitted_task:
        selected_pet = next(pet for pet in owner.get_pets() if pet.name == selected_pet_name)
        selected_pet.add_task(Task(name=task_title, duration=int(duration), priority=priority))
        st.success(f"Added '{task_title}' for {selected_pet_name}!")

st.divider()

st.subheader("Build Schedule")
st.caption("Generates today's schedule from all pets' tasks, based on priority and available time.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner=owner)
    scheduler.generate_schedule()
    scheduler.display_schedule()  # also prints to the terminal running streamlit
    st.session_state.last_schedule = scheduler.schedule

if "last_schedule" in st.session_state:
    st.markdown("### Today's Schedule")
    schedule = st.session_state.last_schedule
    if schedule:
        st.table(
            [
                {
                    "Priority": task.priority.upper(),
                    "Task": task.name,
                    "Pet": task.pet_name or "-",
                    "Duration (min)": task.duration,
                }
                for task in schedule
            ]
        )
    else:
        st.info("No tasks fit in the available time. Add pets/tasks above and try again.")
