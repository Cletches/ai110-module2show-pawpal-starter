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
