import streamlit as st
from pawpal_system import Pet, Task, Owner, Scheduler, Plan

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Initialize application memory (session state)
if "owner" not in st.session_state:
    st.session_state.owner = None  # Will be created when user enters owner info

if "pets" not in st.session_state:
    st.session_state.pets = []  # List of Pet objects

if "current_pet" not in st.session_state:
    st.session_state.current_pet = None  # Currently selected pet

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()  # Scheduler instance

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+, your pet care planning assistant.

This app helps you organize and optimize your daily pet care tasks based on available time, priority, and pet needs.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# === OWNER SETUP ===
st.subheader("📋 Owner Profile")

# Check if an owner already exists in session state vault
if st.session_state.owner:
    st.info(f"📌 **Current Owner (loaded from vault):** {st.session_state.owner.name} | Budget: {st.session_state.owner.daily_time_budget} min")
    owner_name = st.text_input("Owner name", value=st.session_state.owner.name, key="owner_name_input")
    daily_budget = st.number_input(
        "Daily time budget (minutes)", min_value=1, max_value=1440, value=st.session_state.owner.daily_time_budget, key="daily_budget_input"
    )
    if st.button("Update Owner Profile"):
        st.session_state.owner.name = owner_name
        st.session_state.owner.daily_time_budget = daily_budget
        st.success(f"✅ Owner profile updated: {owner_name} (Budget: {daily_budget} min)")
else:
    # No owner exists yet; create one
    owner_name = st.text_input("Owner name", value="Jordan", key="owner_name_input")
    daily_budget = st.number_input(
        "Daily time budget (minutes)", min_value=1, max_value=1440, value=120, key="daily_budget_input"
    )
    if st.button("Create Owner Profile"):
        st.session_state.owner = Owner(
            name=owner_name,
            daily_time_budget=daily_budget,
            pets=st.session_state.pets,
            tasks=[]  # Owner's own tasks
        )
        st.success(f"✅ Owner profile created and vault: {owner_name} (Budget: {daily_budget} min)")

st.divider()

# === PET MANAGEMENT ===
st.subheader("🐾 Manage Pets")

col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi", key="pet_name_input")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "bird", "rabbit", "other"], key="species_input")

if st.button("Add Pet"):
    if st.session_state.owner:
        # Check if a pet with this name already exists in the owner's vault
        existing_pet = st.session_state.owner.get_pet_by_name(pet_name)
        if existing_pet:
            st.warning(f"⚠️ A pet named '{pet_name}' already exists in the vault. Use a different name or update that pet.")
        else:
            new_pet = Pet(name=pet_name, species=species, specific_needs=[], tasks=[])
            st.session_state.owner.add_pet(new_pet)
            st.session_state.pets.append(new_pet)
            st.success(f"✅ Added {pet_name} the {species} to the vault")
    else:
        st.warning("⚠️ Please create an owner profile first.")

if st.session_state.owner and st.session_state.owner.get_pets():
    st.write("**Your Pets (from vault):**")
    for pet in st.session_state.owner.get_pets():
        st.write(f"- {pet.name} ({pet.species}) - {len(pet.tasks)} task(s)")

st.divider()

# === TASK MANAGEMENT ===
st.subheader("✅ Add Tasks to Pets")

if st.session_state.owner and st.session_state.owner.get_pets():
    selected_pet_name = st.selectbox(
        "Select pet", 
        [p.name for p in st.session_state.owner.get_pets()],
        key="pet_selector"
    )
    
    task_title = st.text_input("Task title", value="Morning walk", key="task_title_input")
    task_desc = st.text_area("Task description", value="A morning walk around the neighborhood", key="task_desc_input")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="duration_input")
    with col2:
        priority = st.selectbox("Priority (1=Optional, 5=Critical)", [1, 2, 3, 4, 5], index=4, key="priority_input")
    with col3:
        category = st.selectbox("Category", ["walk", "feeding", "grooming", "play", "meds", "other"], key="category_input")
    
    frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly", "once", "as-needed"], key="frequency_input")
    
    if st.button("Add Task to Pet"):
        selected_pet = st.session_state.owner.get_pet_by_name(selected_pet_name)
        if selected_pet:
            # Check if a task with this title already exists for this pet
            existing_tasks = [t for t in selected_pet.get_tasks() if t.title == task_title]
            if existing_tasks:
                st.warning(f"⚠️ A task named '{task_title}' already exists for {selected_pet_name}. Use a different title or update that task.")
            else:
                new_task = Task(
                    title=task_title,
                    description=task_desc,
                    duration_minutes=int(duration),
                    priority=int(priority),
                    category=category,
                    frequency=frequency,
                    completed=False
                )
                selected_pet.add_task(new_task)
                st.success(f"✅ Added '{task_title}' (vault) to {selected_pet_name}")
        else:
            st.error("Pet not found.")
else:
    st.info("Add a pet first to start adding tasks.")

st.divider()

# === SCHEDULE GENERATION ===
st.subheader("📅 Generate Daily Schedule")

if st.button("Generate Optimized Schedule"):
    if st.session_state.owner:
        plan = st.session_state.scheduler.optimize_plan(st.session_state.owner)
        
        st.success("✨ Schedule generated!")
        
        st.write("### 📋 Today's Plan")
        st.write(f"**Total time allocated:** {plan.total_minutes} / {st.session_state.owner.daily_time_budget} minutes")
        
        if plan.selected_tasks:
            st.write("**Selected tasks (in priority order):**")
            for i, task in enumerate(plan.selected_tasks, 1):
                st.write(f"{i}. **{task.title}** ({task.duration_minutes} min) — Priority: {task.priority}/5 | {task.category}")
        else:
            st.info("No tasks selected for today.")
        
        st.write("### 💡 Plan Explanation")
        st.write(plan.explanation)
    else:
        st.warning("⚠️ Please set up an owner and add pets/tasks first.")
