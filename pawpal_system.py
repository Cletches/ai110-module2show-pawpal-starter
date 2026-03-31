from dataclasses import dataclass, field
from typing import List


@dataclass
class Pet:
	"""Represents a pet profile, its care needs, and associated tasks."""

	name: str
	species: str
	specific_needs: List[str] = field(default_factory=list)
	tasks: List["Task"] = field(default_factory=list)

	def update_needs(self, needs: List[str]) -> None:
		"""Replace the pet's specific needs list."""
		self.specific_needs = list(needs)

	def add_task(self, task: "Task") -> None:
		"""Add a task to the pet's care plan."""
		self.tasks.append(task)

	def remove_task(self, title: str) -> None:
		"""Remove a task by title from the pet's care plan."""
		self.tasks = [t for t in self.tasks if t.title != title]

	def get_tasks(self) -> List["Task"]:
		"""Return all tasks associated with this pet."""
		return list(self.tasks)

	def get_tasks_by_category(self, category: str) -> List["Task"]:
		"""Return tasks filtered by category."""
		return [t for t in self.tasks if t.category.lower() == category.lower()]


@dataclass
class Task:
	"""Represents a single care activity in the owner's plan."""

	title: str
	description: str
	duration_minutes: int
	priority: int
	category: str
	frequency: str
	completed: bool = False

	def __post_init__(self) -> None:
		"""Validate task fields after initialization."""
		if self.duration_minutes <= 0:
			raise ValueError(f"duration_minutes must be positive, got {self.duration_minutes}")
		if not self.title or not self.title.strip():
			raise ValueError("title cannot be empty")
		if not self.description or not self.description.strip():
			raise ValueError("description cannot be empty")
		if not self.is_valid_priority():
			raise ValueError(f"priority must be 1-5, got {self.priority}")
		if not self.frequency or not self.frequency.strip():
			raise ValueError("frequency cannot be empty")
		if self.frequency.lower() not in ["daily", "weekly", "monthly", "once", "as-needed"]:
			raise ValueError(f"frequency must be one of: daily, weekly, monthly, once, as-needed. Got {self.frequency}")

	def is_valid_priority(self) -> bool:
		"""Return True when the task priority is inside the 1-5 range."""
		return 1 <= self.priority <= 5

	def mark_completed(self) -> None:
		"""Mark this task as completed."""
		self.completed = True

	def mark_incomplete(self) -> None:
		"""Mark this task as not completed."""
		self.completed = False


@dataclass
class Plan:
	"""Represents a generated daily schedule with explanation."""

	selected_tasks: List[Task]
	explanation: str
	total_minutes: int


@dataclass
class Owner:
	"""Represents the pet owner, manages multiple pets, and daily planning constraints."""

	name: str
	daily_time_budget: int
	pets: List[Pet] = field(default_factory=list)
	tasks: List[Task] = field(default_factory=list)

	def set_daily_time_budget(self, minutes: int) -> None:
		"""Set the owner's total time budget for a day."""
		self.daily_time_budget = minutes

	def add_pet(self, pet: Pet) -> None:
		"""Add a pet to the owner's household."""
		self.pets.append(pet)

	def remove_pet(self, pet_name: str) -> None:
		"""Remove a pet by name from the owner's household."""
		self.pets = [p for p in self.pets if p.name != pet_name]

	def get_pets(self) -> List[Pet]:
		"""Return all pets managed by this owner."""
		return list(self.pets)

	def get_pet_by_name(self, pet_name: str) -> Pet:
		"""Return a specific pet by name, or None if not found."""
		for pet in self.pets:
			if pet.name == pet_name:
				return pet
		return None

	def get_all_pet_tasks(self) -> List[Task]:
		"""Return all tasks from all pets."""
		all_tasks = []
		for pet in self.pets:
			all_tasks.extend(pet.get_tasks())
		return all_tasks

	def get_all_pet_tasks_by_category(self, category: str) -> List[Task]:
		"""Return all tasks from all pets filtered by category."""
		all_tasks = self.get_all_pet_tasks()
		return [t for t in all_tasks if t.category.lower() == category.lower()]

	def add_task(self, task: Task) -> None:
		"""Add a general task to the owner's task list."""
		self.tasks.append(task)

	def remove_task(self, title: str) -> None:
		"""Remove a task by title from the owner's task list."""
		self.tasks = [t for t in self.tasks if t.title != title]

	def edit_task(self, title: str, updated_task: Task) -> None:
		"""Replace a task by title with an updated version."""
		for i, task in enumerate(self.tasks):
			if task.title == title:
				self.tasks[i] = updated_task
				return


class Scheduler:
	"""Scheduling engine that builds a daily plan from tasks and constraints."""

	def optimize_plan(self, owner: Owner) -> Plan:
		"""
		Generate an optimized daily plan from all owner's tasks (owner + all pets).
		Returns a Plan that respects the owner's time budget.

		Strategy:
		1. Retrieve all available tasks from owner + all pets
		2. Sort by priority (highest first)
		3. Greedily select tasks that fit within the time budget
		4. Generate explanation for the chosen tasks
		"""
		# Gather all available tasks
		owner_tasks = owner.tasks
		pet_tasks = owner.get_all_pet_tasks()
		all_available_tasks = owner_tasks + pet_tasks

		# Get the time constraint
		time_budget = owner.daily_time_budget

		# Select tasks that fit within the budget
		selected_tasks = self._select_tasks(all_available_tasks, time_budget)

		# Calculate total time and generate explanation
		total_minutes = self.calculate_total_duration(selected_tasks)
		explanation = self._explain_choices(selected_tasks, owner, all_available_tasks, time_budget)

		return Plan(selected_tasks, explanation, total_minutes)

	def _select_tasks(self, tasks: List[Task], time_budget: int) -> List[Task]:
		"""
		Greedily select tasks by priority that fit within the time budget.
		Returns a list of selected tasks.
		"""
		if not tasks:
			return []

		# Sort by priority (highest first)
		prioritized = self.sort_by_priority(tasks)

		selected = []
		used_time = 0

		for task in prioritized:
			# If task fits within budget, include it
			if used_time + task.duration_minutes <= time_budget:
				selected.append(task)
				used_time += task.duration_minutes

		return selected

	def _explain_choices(self, selected_tasks: List[Task], owner: Owner, all_tasks: List[Task], time_budget: int) -> str:
		"""
		Generate a human-readable explanation of why these tasks were selected.
		"""
		if not selected_tasks:
			return f"No tasks could fit within the {time_budget} minute budget. Consider reducing task durations or extending your available time."

		total_selected = self.calculate_total_duration(selected_tasks)
		remaining_time = time_budget - total_selected

		# Build explanation
		lines = [f"Daily plan for {owner.name} ({total_selected} of {time_budget} minutes):"]
		lines.append("")

		# List selected tasks with their priority and duration
		for task in selected_tasks:
			priority_label = self._priority_label(task.priority)
			lines.append(f"  • {task.title} ({task.duration_minutes} min) - Priority: {priority_label}")

		lines.append("")
		lines.append(f"Remaining time: {remaining_time} minutes")

		# Explain why other high-priority tasks weren't selected
		excluded_high_priority = [
			t for t in all_tasks
			if t not in selected_tasks and t.priority >= 4
		]

		if excluded_high_priority:
			lines.append("")
			lines.append("Note: The following high-priority tasks did not fit:")
			for task in excluded_high_priority[:3]:  # Show top 3
				lines.append(f"  • {task.title} ({task.duration_minutes} min) - Priority: {self._priority_label(task.priority)}")

		return "\n".join(lines)

	def _priority_label(self, priority: int) -> str:
		"""Convert numerical priority to readable label."""
		labels = {
			5: "Critical",
			4: "High",
			3: "Medium",
			2: "Low",
			1: "Optional"
		}
		return labels.get(priority, "Unknown")

	def calculate_total_duration(self, tasks: List[Task]) -> int:
		"""Return the total duration for a task list in minutes."""
		return sum(task.duration_minutes for task in tasks)

	def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
		"""Return tasks sorted by priority descending (higher first)."""
		return sorted(tasks, key=lambda task: task.priority, reverse=True)
