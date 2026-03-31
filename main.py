"""
PawPal+ Demo Script
Demonstrates the full pet care planning system with Owner, Pets, Tasks, and Scheduler.
"""

from pawpal_system import Pet, Task, Owner, Scheduler


def main():
    print("=" * 60)
    print("🐾 PawPal+ Daily Schedule Planner")
    print("=" * 60)
    print()

    # ========== CREATE OWNER ==========
    owner = Owner(
        name="Alex",
        daily_time_budget=120,  # 120 minutes available today
        pets=[],
        tasks=[]
    )
    print(f"📋 Owner: {owner.name}")
    print(f"⏱️  Daily Time Budget: {owner.daily_time_budget} minutes")
    print()

    # ========== CREATE PETS ==========
    dog = Pet(
        name="Max",
        species="Golden Retriever",
        specific_needs=["exercise", "socialization"],
        tasks=[]
    )
    
    cat = Pet(
        name="Whiskers",
        species="Siamese Cat",
        specific_needs=["playtime", "grooming"],
        tasks=[]
    )
    
    owner.add_pet(dog)
    owner.add_pet(cat)
    print(f"🐕 Pets: {', '.join([p.name for p in owner.get_pets()])}")
    print()

    scheduler = Scheduler()

    # ========== CREATE TASKS FOR DOG (INTENTIONALLY OUT OF ORDER) ==========
    morning_walk = Task(
        title="Morning Walk",
        description="30-minute walk around the neighborhood",
        duration_minutes=30,
        priority=5,  # Critical
        category="exercise",
        frequency="daily",
        completed=False
    )
    morning_walk.time = "07:30"
    
    play_fetch = Task(
        title="Play Fetch",
        description="Interactive fetch game at the park",
        duration_minutes=25,
        priority=4,  # High
        category="exercise",
        frequency="daily",
        completed=False
    )
    play_fetch.time = "18:00"

    quick_brush = Task(
        title="Quick Brush",
        description="Short coat brushing session",
        duration_minutes=10,
        priority=4,
        category="grooming",
        frequency="daily",
        completed=False
    )
    quick_brush.time = "12:15"
    
    dog.add_task(play_fetch)
    dog.add_task(quick_brush)
    dog.add_task(morning_walk)
    print(f"🐕 Max's Tasks:")
    for task in dog.get_tasks():
        print(f"   • {task.time} - {task.title} ({task.duration_minutes} min, Priority: {task.priority})")
    print()

    # ========== CREATE TASKS FOR CAT (INTENTIONALLY OUT OF ORDER) ==========
    grooming = Task(
        title="Grooming Session",
        description="Brush fur and trim nails",
        duration_minutes=20,
        priority=3,  # Medium
        category="grooming",
        frequency="weekly",
        completed=False
    )
    grooming.time = "20:15"
    
    playtime = Task(
        title="Interactive Play",
        description="Play with laser pointer and toy mouse",
        duration_minutes=15,
        priority=4,  # High
        category="playtime",
        frequency="daily",
        completed=False
    )
    # Intentional overlap with Max's "Play Fetch" to demo conflict warnings.
    playtime.time = "18:00"
    
    feeding = Task(
        title="Meal Prep & Feeding",
        description="Prepare food bowls and feed Whiskers",
        duration_minutes=10,
        priority=5,  # Critical
        category="feeding",
        frequency="daily",
        completed=False
    )
    feeding.time = "08:00"

    litter_check = Task(
        title="Litter Box Check",
        description="Clean and refresh litter box",
        duration_minutes=12,
        priority=3,
        category="hygiene",
        frequency="daily",
        completed=False
    )
    litter_check.time = "06:45"
    
    cat.add_task(playtime)
    cat.add_task(litter_check)
    cat.add_task(grooming)
    cat.add_task(feeding)
    print(f"🐱 Whiskers's Tasks:")
    for task in cat.get_tasks():
        print(f"   • {task.time} - {task.title} ({task.duration_minutes} min, Priority: {task.priority})")
    print()

    # ========== DEMO: SORT TASKS BY TIME ==========
    print("=" * 60)
    print("🕒 TASKS SORTED BY TIME (ALL PETS)")
    print("=" * 60)
    print()
    all_pet_tasks = owner.get_all_pet_tasks()
    for task in scheduler.sort_by_time(all_pet_tasks):
        print(f"   • {task.time} - {task.title} ({task.category})")
    print()

    # ========== DEMO: FILTER TASKS ==========
    # Mark one task completed so both filter modes are visible.
    play_fetch.mark_completed()

    print("=" * 60)
    print("🔎 FILTERED TASKS")
    print("=" * 60)
    print()

    completed_tasks = owner.filter_tasks(completed=True)
    print("✅ Completed Tasks:")
    if completed_tasks:
        for task in completed_tasks:
            print(f"   • {task.title}")
    else:
        print("   • None")
    print()

    whiskers_open_tasks = owner.filter_tasks(completed=False, pet_name="Whiskers")
    print("🐱 Whiskers Incomplete Tasks:")
    if whiskers_open_tasks:
        for task in whiskers_open_tasks:
            print(f"   • {task.title}")
    else:
        print("   • None")
    print()

    # ========== DEMO: LIGHTWEIGHT CONFLICT WARNING ==========
    warning = scheduler.get_conflict_warning(owner)
    print("=" * 60)
    print("⚠️  CONFLICT CHECK")
    print("=" * 60)
    if warning:
        print(warning)
    else:
        print("No scheduling conflicts found.")
    print()

    # ========== GENERATE TODAY'S SCHEDULE ==========
    plan = scheduler.optimize_plan(owner)
    
    print("=" * 60)
    print("📅 TODAY'S OPTIMIZED SCHEDULE")
    print("=" * 60)
    print()
    
    if plan.selected_tasks:
        print("✅ Selected Tasks:")
        total_time = 0
        for i, task in enumerate(plan.selected_tasks, 1):
            print(f"   {i}. {task.title} ({task.duration_minutes} min) - Priority: {task.priority}")
            total_time += task.duration_minutes
        print()
        print(f"⏱️  Total Time Required: {plan.total_minutes} minutes")
        print(f"🕐 Time Remaining: {owner.daily_time_budget - plan.total_minutes} minutes")
        print()
        print("📝 Plan Explanation:")
        print(f"   {plan.explanation}")
    else:
        print("❌ No tasks could fit in today's schedule.")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
