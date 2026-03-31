from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Optional


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

	def mark_completed(self, task_collection: Optional[List["Task"]] = None) -> Optional["Task"]:
		"""
		Mark this task as completed.

		For recurring tasks with frequency "daily" or "weekly", automatically
		create the next occurrence. If task_collection is provided, that new task
		is appended to the collection.

		If an optional dynamic due_date attribute exists, this method advances it
		for the new occurrence: +1 day for daily, +7 days for weekly.
		"""
		self.completed = True

		if self.frequency.lower() not in ["daily", "weekly"]:
			return None

		next_task = Task(
			title=self.title,
			description=self.description,
			duration_minutes=self.duration_minutes,
			priority=self.priority,
			category=self.category,
			frequency=self.frequency,
			completed=False,
		)

		# Preserve optional dynamic HH:MM time if the task has one.
		if hasattr(self, "time"):
			next_task.time = self.time

		# Advance optional dynamic due_date for recurring tasks when possible.
		if hasattr(self, "due_date"):
			delta_days = 1 if self.frequency.lower() == "daily" else 7
			due_date_value = getattr(self, "due_date")
			if isinstance(due_date_value, datetime):
				next_task.due_date = due_date_value + timedelta(days=delta_days)
			elif isinstance(due_date_value, date):
				next_task.due_date = due_date_value + timedelta(days=delta_days)
			elif isinstance(due_date_value, str):
				try:
					parsed = datetime.fromisoformat(due_date_value)
					next_task.due_date = (parsed + timedelta(days=delta_days)).date().isoformat()
				except ValueError:
					# Keep original value when format is unknown.
					next_task.due_date = due_date_value
			else:
				next_task.due_date = due_date_value

		if task_collection is not None:
			task_collection.append(next_task)

		return next_task

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

	def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
		"""
		Return tasks filtered by completion status and/or pet name.

		- If pet_name is provided, only tasks for that pet are considered.
		- If pet_name is omitted, owner tasks and all pet tasks are considered.
		- If completed is provided, only tasks matching that completion status are returned.
		"""
		if pet_name:
			pet = self.get_pet_by_name(pet_name)
			if pet is None:
				return []
			candidate_tasks = pet.get_tasks()
		else:
			candidate_tasks = list(self.tasks) + self.get_all_pet_tasks()

		if completed is None:
			return candidate_tasks

		return [task for task in candidate_tasks if task.completed is completed]

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

	def get_conflict_warning(self, owner: Owner) -> Optional[str]:
		"""
		Return a non-fatal warning message when schedule conflicts are found.

		Args:
			owner: Owner whose pet tasks should be analyzed.

		Returns:
			A warning string when one or more conflicts are detected, None when no
			conflicts exist, or a fallback warning if conflict analysis cannot run
			safely due to invalid input data.

		Notes:
			This method is intentionally lightweight and defensive. It catches
			unexpected exceptions from conflict analysis so callers can display a
			message without crashing the program flow.
		"""
		try:
			conflicts = self.detect_time_conflicts(owner)
		except Exception:
			return "Warning: Could not evaluate scheduling conflicts due to invalid task data."

		if not conflicts:
			return None

		first = conflicts[0]
		conflict_count = len(conflicts)
		return (
			f"Warning: Found {conflict_count} scheduling conflict(s). "
			f"Example at {first['time']}: {first['pet_1']} - {first['task_1']} overlaps with "
			f"{first['pet_2']} - {first['task_2']}."
		)

	def detect_time_conflicts(self, owner: Owner) -> List[dict]:
		"""
		Detect pairwise task conflicts for tasks that share the same HH:MM value.

		Args:
			owner: Owner whose pets and tasks are scanned for timed overlaps.

		Returns:
			A list of conflict dictionaries. Each dictionary includes:
			- time: normalized HH:MM string
			- pet_1, task_1: first conflicting task
			- pet_2, task_2: second conflicting task
			- same_pet: True if both tasks belong to the same pet

		Algorithm:
			Single-pass grouping by time. For each timed task, compare against
			already-seen tasks for that same time and emit conflict pairs.
		"""
		conflicts = []
		tasks_by_time = {}

		for pet in owner.get_pets():
			for task in pet.get_tasks():
				task_time = getattr(task, "time", None)
				if not task_time:
					continue

				normalized_time = str(task_time).strip()
				if not normalized_time:
					continue

				current_item = {
					"pet": pet.name,
					"task": task.title,
					"time": normalized_time,
				}

				for existing_item in tasks_by_time.get(normalized_time, []):
					conflicts.append(
						{
							"time": normalized_time,
							"pet_1": existing_item["pet"],
							"task_1": existing_item["task"],
							"pet_2": current_item["pet"],
							"task_2": current_item["task"],
							"same_pet": existing_item["pet"] == current_item["pet"],
						}
					)

				tasks_by_time.setdefault(normalized_time, []).append(current_item)

		return conflicts

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
		For tasks with equal priority, prefer shorter tasks first so more
		tasks can fit into the same budget.
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
		selected_task_ids = {id(task) for task in selected_tasks}
		excluded_high_priority = [
			t for t in all_tasks
			if id(t) not in selected_task_ids and t.priority >= 4
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
		"""Return tasks sorted by priority descending, then duration ascending."""
		return sorted(tasks, key=lambda task: (-task.priority, task.duration_minutes))

	def sort_by_time(self, tasks: List[Task]) -> List[Task]:
		"""Return tasks sorted by their time attribute in HH:MM format."""
		return sorted(
			tasks,
			key=lambda task: tuple(int(part) for part in task.time.split(":"))
		)
