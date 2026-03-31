from dataclasses import dataclass, field
from typing import List


@dataclass
class Pet:
	"""Represents a pet profile and its care needs."""

	name: str
	species: str
	specific_needs: List[str] = field(default_factory=list)

	def update_needs(self, needs: List[str]) -> None:
		"""Replace the pet's specific needs list."""
		self.specific_needs = list(needs)


@dataclass
class Task:
	"""Represents a single care activity in the owner's plan."""

	title: str
	duration_minutes: int
	priority: int
	category: str

	def is_valid_priority(self) -> bool:
		"""Return True when the task priority is inside the 1-5 range."""
		return 1 <= self.priority <= 5


@dataclass
class Owner:
	"""Represents the pet owner and daily planning constraints."""

	name: str
	daily_time_budget: int
	pet: Pet

	def set_daily_time_budget(self, minutes: int) -> None:
		"""Set the owner's total time budget for a day."""
		self.daily_time_budget = minutes

	def get_pet_profile(self) -> Pet:
		"""Return the owner's pet profile."""
		return self.pet


class Scheduler:
	"""Scheduling engine that builds a daily plan from tasks and constraints."""

	def optimize_plan(self, tasks: List[Task], time_budget: int) -> List[Task]:
		"""Return an optimized list of tasks that fit inside the given time budget."""
		raise NotImplementedError("Implement scheduling logic in optimize_plan.")

	def calculate_total_duration(self, tasks: List[Task]) -> int:
		"""Return the total duration for a task list in minutes."""
		return sum(task.duration_minutes for task in tasks)

	def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
		"""Return tasks sorted by priority descending (higher first)."""
		return sorted(tasks, key=lambda task: task.priority, reverse=True)
