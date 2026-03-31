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

    # ========== CREATE TASKS FOR DOG ==========
    morning_walk = Task(
        title="Morning Walk",
        description="30-minute walk around the neighborhood",
        duration_minutes=30,
        priority=5,  # Critical
        category="exercise",
        frequency="daily",
        completed=False
    )
    
    play_fetch = Task(
        title="Play Fetch",
        description="Interactive fetch game at the park",
        duration_minutes=25,
        priority=4,  # High
        category="exercise",
        frequency="daily",
        completed=False
    )
    
    dog.add_task(morning_walk)
    dog.add_task(play_fetch)
    print(f"🐕 Max's Tasks:")
    for task in dog.get_tasks():
        print(f"   • {task.title} ({task.duration_minutes} min, Priority: {task.priority})")
    print()

    # ========== CREATE TASKS FOR CAT ==========
    grooming = Task(
        title="Grooming Session",
        description="Brush fur and trim nails",
        duration_minutes=20,
        priority=3,  # Medium
        category="grooming",
        frequency="weekly",
        completed=False
    )
    
    playtime = Task(
        title="Interactive Play",
        description="Play with laser pointer and toy mouse",
        duration_minutes=15,
        priority=4,  # High
        category="playtime",
        frequency="daily",
        completed=False
    )
    
    feeding = Task(
        title="Meal Prep & Feeding",
        description="Prepare food bowls and feed Whiskers",
        duration_minutes=10,
        priority=5,  # Critical
        category="feeding",
        frequency="daily",
        completed=False
    )
    
    cat.add_task(grooming)
    cat.add_task(playtime)
    cat.add_task(feeding)
    print(f"🐱 Whiskers's Tasks:")
    for task in cat.get_tasks():
        print(f"   • {task.title} ({task.duration_minutes} min, Priority: {task.priority})")
    print()

    # ========== GENERATE TODAY'S SCHEDULE ==========
    scheduler = Scheduler()
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
