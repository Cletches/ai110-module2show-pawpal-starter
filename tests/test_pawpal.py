import pytest
import sys
from pathlib import Path

# Add parent directory to path so we can import pawpal_system
sys.path.insert(0, str(Path(__file__).parent.parent))

from pawpal_system import Pet, Task, Owner, Scheduler


class TestTaskCompletion:
    """Test Task completion status tracking."""
    
    def test_mark_completed_changes_status(self):
        """Verify that calling mark_completed() changes task's completed status to True."""
        # Arrange
        task = Task(
            title="Morning Walk",
            description="A 30-minute walk around the park",
            duration_minutes=30,
            priority=5,
            category="exercise",
            frequency="daily",
            completed=False
        )
        
        # Act
        task.mark_completed()
        
        # Assert
        assert task.completed is True, "Task should be marked as completed"
    
    def test_mark_incomplete_changes_status(self):
        """Verify that calling mark_incomplete() changes task's completed status to False."""
        # Arrange
        task = Task(
            title="Feeding Time",
            description="Feed the pet their daily meal",
            duration_minutes=15,
            priority=5,
            category="feeding",
            frequency="daily",
            completed=True
        )
        
        # Act
        task.mark_incomplete()
        
        # Assert
        assert task.completed is False, "Task should be marked as incomplete"

    def test_mark_completed_daily_task_creates_next_occurrence(self):
        """Daily task completion should auto-create the next pending occurrence."""
        # Arrange
        task = Task(
            title="Morning Walk",
            description="Walk around the block",
            duration_minutes=30,
            priority=5,
            category="exercise",
            frequency="daily",
            completed=False,
        )
        task_list = [task]

        # Act
        next_task = task.mark_completed(task_collection=task_list)

        # Assert
        assert task.completed is True
        assert next_task is not None
        assert next_task in task_list
        assert next_task is not task
        assert next_task.completed is False
        assert next_task.frequency == "daily"

    def test_mark_completed_weekly_task_creates_next_occurrence(self):
        """Weekly task completion should auto-create the next pending occurrence."""
        # Arrange
        task = Task(
            title="Grooming",
            description="Brush and nail trim",
            duration_minutes=20,
            priority=4,
            category="grooming",
            frequency="weekly",
            completed=False,
        )
        task_list = [task]

        # Act
        next_task = task.mark_completed(task_collection=task_list)

        # Assert
        assert task.completed is True
        assert next_task is not None
        assert next_task in task_list
        assert next_task.completed is False
        assert next_task.frequency == "weekly"

    def test_mark_completed_once_task_does_not_create_next_occurrence(self):
        """Non-recurring tasks should not generate follow-up tasks."""
        # Arrange
        task = Task(
            title="Vet Appointment",
            description="Annual checkup",
            duration_minutes=60,
            priority=5,
            category="health",
            frequency="once",
            completed=False,
        )
        task_list = [task]

        # Act
        next_task = task.mark_completed(task_collection=task_list)

        # Assert
        assert task.completed is True
        assert next_task is None
        assert len(task_list) == 1


class TestTaskAddition:
    """Test Task addition to a Pet."""
    
    def test_adding_task_to_pet_increases_task_count(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        # Arrange
        pet = Pet(name="Max", species="Golden Retriever", specific_needs=["daily exercise"])
        initial_count = len(pet.tasks)
        
        task = Task(
            title="Play Fetch",
            description="Throw a ball for 20 minutes",
            duration_minutes=20,
            priority=4,
            category="exercise",
            frequency="daily",
            completed=False
        )
        
        # Act
        pet.add_task(task)
        final_count = len(pet.tasks)
        
        # Assert
        assert final_count == initial_count + 1, "Pet's task count should increase by 1"
        assert task in pet.tasks, "Task should be in pet's task list"
    
    def test_adding_multiple_tasks_increments_count(self):
        """Verify that adding multiple tasks increments the task count correctly."""
        # Arrange
        pet = Pet(name="Whiskers", species="Siamese Cat", specific_needs=["grooming"])
        
        task1 = Task(
            title="Grooming",
            description="Brush the cat's fur",
            duration_minutes=20,
            priority=3,
            category="grooming",
            frequency="weekly",
            completed=False
        )
        
        task2 = Task(
            title="Interactive Play",
            description="Play with toys for enrichment",
            duration_minutes=15,
            priority=4,
            category="exercise",
            frequency="daily",
            completed=False
        )
        
        # Act
        pet.add_task(task1)
        pet.add_task(task2)
        
        # Assert
        assert len(pet.tasks) == 2, "Pet should have 2 tasks"
        assert task1 in pet.tasks, "First task should be in pet's task list"
        assert task2 in pet.tasks, "Second task should be in pet's task list"


class TestScheduler:
    """Test scheduling prioritization and time-budget selection behavior."""

    def test_get_conflict_warning_returns_message_when_conflict_exists(self):
        """Lightweight conflict check should return a warning string for overlaps."""
        # Arrange
        scheduler = Scheduler()
        owner = Owner(name="Alex", daily_time_budget=120)
        pet = Pet(name="Max", species="dog")
        owner.add_pet(pet)

        task_1 = Task(
            title="Morning Walk",
            description="Walk around the block",
            duration_minutes=20,
            priority=5,
            category="exercise",
            frequency="daily",
        )
        task_2 = Task(
            title="Breakfast",
            description="Feed breakfast",
            duration_minutes=10,
            priority=5,
            category="feeding",
            frequency="daily",
        )

        task_1.time = "08:00"
        task_2.time = "08:00"
        pet.add_task(task_1)
        pet.add_task(task_2)

        # Act
        warning = scheduler.get_conflict_warning(owner)

        # Assert
        assert warning is not None
        assert "Warning:" in warning
        assert "08:00" in warning

    def test_get_conflict_warning_returns_none_when_no_conflict(self):
        """Lightweight conflict check should return None when there is no overlap."""
        # Arrange
        scheduler = Scheduler()
        owner = Owner(name="Alex", daily_time_budget=120)
        pet = Pet(name="Max", species="dog")
        owner.add_pet(pet)

        task_1 = Task(
            title="Morning Walk",
            description="Walk around the block",
            duration_minutes=20,
            priority=5,
            category="exercise",
            frequency="daily",
        )
        task_2 = Task(
            title="Evening Feed",
            description="Feed dinner",
            duration_minutes=10,
            priority=5,
            category="feeding",
            frequency="daily",
        )

        task_1.time = "08:00"
        task_2.time = "18:00"
        pet.add_task(task_1)
        pet.add_task(task_2)

        # Act
        warning = scheduler.get_conflict_warning(owner)

        # Assert
        assert warning is None

    def test_get_conflict_warning_handles_invalid_owner_without_crashing(self):
        """Lightweight conflict check should return fallback warning instead of raising."""
        # Arrange
        scheduler = Scheduler()

        # Act
        warning = scheduler.get_conflict_warning(None)

        # Assert
        assert warning == "Warning: Could not evaluate scheduling conflicts due to invalid task data."

    def test_detect_time_conflicts_within_same_pet(self):
        """Scheduler should detect two tasks at the same time for one pet."""
        # Arrange
        scheduler = Scheduler()
        owner = Owner(name="Alex", daily_time_budget=120)
        pet = Pet(name="Max", species="dog")
        owner.add_pet(pet)

        task_1 = Task(
            title="Morning Walk",
            description="Walk around the block",
            duration_minutes=20,
            priority=5,
            category="exercise",
            frequency="daily",
        )
        task_2 = Task(
            title="Breakfast",
            description="Feed breakfast",
            duration_minutes=10,
            priority=5,
            category="feeding",
            frequency="daily",
        )

        task_1.time = "08:00"
        task_2.time = "08:00"
        pet.add_task(task_1)
        pet.add_task(task_2)

        # Act
        conflicts = scheduler.detect_time_conflicts(owner)

        # Assert
        assert len(conflicts) == 1
        assert conflicts[0]["time"] == "08:00"
        assert conflicts[0]["same_pet"] is True
        assert {conflicts[0]["task_1"], conflicts[0]["task_2"]} == {"Morning Walk", "Breakfast"}

    def test_detect_time_conflicts_across_pets(self):
        """Scheduler should detect same-time tasks belonging to different pets."""
        # Arrange
        scheduler = Scheduler()
        owner = Owner(name="Alex", daily_time_budget=120)
        dog = Pet(name="Max", species="dog")
        cat = Pet(name="Milo", species="cat")
        owner.add_pet(dog)
        owner.add_pet(cat)

        dog_task = Task(
            title="Dog Walk",
            description="Walk in park",
            duration_minutes=25,
            priority=4,
            category="exercise",
            frequency="daily",
        )
        cat_task = Task(
            title="Cat Feed",
            description="Feed breakfast",
            duration_minutes=10,
            priority=5,
            category="feeding",
            frequency="daily",
        )

        dog_task.time = "07:30"
        cat_task.time = "07:30"
        dog.add_task(dog_task)
        cat.add_task(cat_task)

        # Act
        conflicts = scheduler.detect_time_conflicts(owner)

        # Assert
        assert len(conflicts) == 1
        assert conflicts[0]["time"] == "07:30"
        assert conflicts[0]["same_pet"] is False
        assert {conflicts[0]["pet_1"], conflicts[0]["pet_2"]} == {"Max", "Milo"}

    def test_detect_time_conflicts_returns_empty_when_no_overlap(self):
        """Scheduler should return no conflicts when task times do not overlap."""
        # Arrange
        scheduler = Scheduler()
        owner = Owner(name="Alex", daily_time_budget=120)
        pet = Pet(name="Max", species="dog")
        owner.add_pet(pet)

        task_1 = Task(
            title="Morning Walk",
            description="Walk around the block",
            duration_minutes=20,
            priority=5,
            category="exercise",
            frequency="daily",
        )
        task_2 = Task(
            title="Evening Feed",
            description="Feed dinner",
            duration_minutes=10,
            priority=5,
            category="feeding",
            frequency="daily",
        )

        task_1.time = "08:00"
        task_2.time = "18:00"
        pet.add_task(task_1)
        pet.add_task(task_2)

        # Act
        conflicts = scheduler.detect_time_conflicts(owner)

        # Assert
        assert conflicts == []

    def test_sort_by_priority_breaks_ties_with_shorter_duration_first(self):
        """Equal-priority tasks should be sorted shortest duration first."""
        # Arrange
        scheduler = Scheduler()
        long_task = Task(
            title="Long Play Session",
            description="Extended play time",
            duration_minutes=30,
            priority=4,
            category="playtime",
            frequency="daily"
        )
        short_task = Task(
            title="Quick Training Drill",
            description="Short focused training",
            duration_minutes=10,
            priority=4,
            category="training",
            frequency="daily"
        )

        # Act
        sorted_tasks = scheduler.sort_by_priority([long_task, short_task])

        # Assert
        assert sorted_tasks[0] == short_task
        assert sorted_tasks[1] == long_task

    def test_optimize_plan_fits_more_equal_priority_tasks_when_possible(self):
        """Tie-breaking by shorter duration should improve packing into the budget."""
        # Arrange
        owner = Owner(name="Alex", daily_time_budget=20)
        scheduler = Scheduler()

        long_task = Task(
            title="Long Walk",
            description="Long neighborhood walk",
            duration_minutes=15,
            priority=4,
            category="exercise",
            frequency="daily"
        )
        short_task_1 = Task(
            title="Treat Puzzle",
            description="Quick enrichment game",
            duration_minutes=10,
            priority=4,
            category="enrichment",
            frequency="daily"
        )
        short_task_2 = Task(
            title="Recall Drill",
            description="Short recall training",
            duration_minutes=10,
            priority=4,
            category="training",
            frequency="daily"
        )

        owner.add_task(long_task)
        owner.add_task(short_task_1)
        owner.add_task(short_task_2)

        # Act
        plan = scheduler.optimize_plan(owner)

        # Assert
        assert long_task not in plan.selected_tasks
        assert short_task_1 in plan.selected_tasks
        assert short_task_2 in plan.selected_tasks
        assert plan.total_minutes == 20

    def test_sort_by_time_orders_tasks_by_hh_mm(self):
        """Tasks should be sorted chronologically by HH:MM time string."""
        # Arrange
        scheduler = Scheduler()
        task_morning = Task(
            title="Morning Feed",
            description="Feed breakfast",
            duration_minutes=15,
            priority=5,
            category="feeding",
            frequency="daily"
        )
        task_midday = Task(
            title="Midday Walk",
            description="Short walk",
            duration_minutes=20,
            priority=4,
            category="exercise",
            frequency="daily"
        )
        task_evening = Task(
            title="Evening Groom",
            description="Quick brush",
            duration_minutes=10,
            priority=3,
            category="grooming",
            frequency="daily"
        )

        # Dynamically add a time attribute in HH:MM format.
        task_evening.time = "18:30"
        task_morning.time = "07:45"
        task_midday.time = "12:00"

        # Act
        sorted_tasks = scheduler.sort_by_time([task_evening, task_morning, task_midday])

        # Assert
        assert [t.title for t in sorted_tasks] == [
            "Morning Feed",
            "Midday Walk",
            "Evening Groom",
        ]


class TestOwnerTaskFiltering:
    """Test filtering owner/pet tasks by completion status and pet name."""

    def test_filter_tasks_by_completion_status(self):
        """Owner should be able to filter all tasks by completion state."""
        # Arrange
        owner = Owner(name="Alex", daily_time_budget=120)
        pet = Pet(name="Max", species="dog")
        owner.add_pet(pet)

        owner_task = Task(
            title="Refill Treat Jar",
            description="Refill treats",
            duration_minutes=5,
            priority=2,
            category="other",
            frequency="weekly",
            completed=False,
        )
        completed_pet_task = Task(
            title="Morning Walk",
            description="Walk around the block",
            duration_minutes=20,
            priority=5,
            category="exercise",
            frequency="daily",
            completed=True,
        )

        owner.add_task(owner_task)
        pet.add_task(completed_pet_task)

        # Act
        completed_tasks = owner.filter_tasks(completed=True)
        incomplete_tasks = owner.filter_tasks(completed=False)

        # Assert
        assert completed_tasks == [completed_pet_task]
        assert incomplete_tasks == [owner_task]

    def test_filter_tasks_by_pet_name(self):
        """Filtering by pet should only return tasks for that specific pet."""
        # Arrange
        owner = Owner(name="Alex", daily_time_budget=120)
        dog = Pet(name="Max", species="dog")
        cat = Pet(name="Milo", species="cat")
        owner.add_pet(dog)
        owner.add_pet(cat)

        dog_task = Task(
            title="Dog Walk",
            description="Walk in park",
            duration_minutes=25,
            priority=4,
            category="exercise",
            frequency="daily",
        )
        cat_task = Task(
            title="Cat Groom",
            description="Brush fur",
            duration_minutes=10,
            priority=3,
            category="grooming",
            frequency="weekly",
        )
        dog.add_task(dog_task)
        cat.add_task(cat_task)

        # Act
        max_tasks = owner.filter_tasks(pet_name="Max")
        unknown_pet_tasks = owner.filter_tasks(pet_name="Unknown")

        # Assert
        assert max_tasks == [dog_task]
        assert unknown_pet_tasks == []

    def test_filter_tasks_by_completion_and_pet_name(self):
        """Filtering should support combining completion status with pet selection."""
        # Arrange
        owner = Owner(name="Alex", daily_time_budget=120)
        pet = Pet(name="Max", species="dog")
        owner.add_pet(pet)

        completed_task = Task(
            title="Done Task",
            description="Already done",
            duration_minutes=10,
            priority=3,
            category="other",
            frequency="once",
            completed=True,
        )
        pending_task = Task(
            title="Pending Task",
            description="Still pending",
            duration_minutes=15,
            priority=3,
            category="other",
            frequency="once",
            completed=False,
        )
        pet.add_task(completed_task)
        pet.add_task(pending_task)

        # Act
        completed_for_pet = owner.filter_tasks(completed=True, pet_name="Max")

        # Assert
        assert completed_for_pet == [completed_task]
