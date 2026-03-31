# PawPal+

PawPal+ is a pet care planning app that helps pet owners create realistic daily care schedules.
It combines task priority, time limits, and conflict checks to produce a plan that is practical to follow.

## Overview

PawPal+ lets you:

- Create an owner profile with a daily time budget.
- Add multiple pets and assign care tasks to each pet.
- Generate an optimized daily plan based on priority and available time.
- Detect overlapping task times and show non-blocking warnings.
- Review selected tasks, timed tasks in chronological order, and deferred tasks.

## Features

- Priority-first scheduling: Tasks are selected by priority so essential care is handled first.
- Time-budget enforcement: The plan never exceeds the owner's available daily minutes.
- Tie-break optimization: For equal priority, shorter tasks are chosen first to fit more work when possible.
- Sorting by priority: Selected tasks are displayed in priority order for quick review.
- Sorting by time: Timed tasks are displayed in chronological HH:MM order.
- Conflict detection: Duplicate HH:MM times are detected across all pet tasks.
- Cross-pet overlap awareness: Conflicts are flagged for both same-pet and different-pet overlaps.
- Lightweight conflict warnings: Overlaps generate warnings instead of causing runtime failures.
- Daily recurrence rollover: Completing a daily recurring task can create the next task for the following day.
- Weekly recurrence rollover: Completing a weekly recurring task can create the next task one week later.
- Completion tracking and filtering: Tasks can be marked complete/incomplete and filtered for focused views.

## Core Scheduling Behavior

The scheduler uses a lightweight, transparent strategy:

- Priority-first selection: higher-priority tasks are considered first.
- Time-budget enforcement: selected tasks must fit the owner's daily minutes.
- Tie-breaking: for equal priority, shorter tasks are preferred.
- Time conflict detection: duplicate HH:MM times are flagged for same-pet or cross-pet overlaps.
- Safe warnings: conflicts return warning messages instead of crashing the app.

## Requirements

- Python 3.11+
- Dependencies listed in requirements.txt

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run The App

Start the Streamlit interface:

```bash
streamlit run app.py
```

You can also run the CLI/demo flow:

```bash
python main.py
```

## How To Use PawPal+

1. Create or update the owner profile.
2. Add one or more pets.
3. Add tasks per pet with duration, priority, category, and frequency.
4. Click Generate Optimized Schedule.
5. Review:

- Conflict warnings table (if overlaps exist)
- Selected tasks (priority order)
- Timed tasks (chronological order)
- Deferred tasks (excluded by time/priority tradeoffs)

## Testing PawPal+

Run the full automated test suite:

```bash
python -m pytest
```

Tests cover:

- Task completion and status transitions
- Daily/weekly recurrence behavior
- Sorting correctness (priority and chronological time sorting)
- Time-budget plan selection
- Conflict detection for duplicate times
- Lightweight warning behavior for schedule conflicts

## Project Structure

- app.py: Streamlit user interface
- main.py: command-line demo script
- pawpal_system.py: domain classes and scheduler logic
- tests/test_pawpal.py: unit tests for core behaviors

## Troubleshooting

- Streamlit command not found:
  Install dependencies first with pip install -r requirements.txt.
- No tasks selected in a plan:
  Increase daily budget or lower durations/priorities for current tasks.
- Conflict warnings shown:
  Adjust task times to remove overlapping HH:MM entries.

## Notes

PawPal+ is designed for clarity and reliability. The scheduler favors fast, explainable decisions over heavy optimization so pet owners can trust and act on the output quickly.

## Demo

### Overview Screen

![Owner and Pet Setup](Pet%20Care%20Task%20Optimization-2026-03-31-171215.png)
Overview of the owner profile and pet setup interface.

### Task Selection and Conflict Warnings

![Task Selection](Screenshot%202026-03-31%20at%2012.16.25%20PM.png)
Selected tasks with conflict detection warnings displayed.

### Scheduling Results

![Schedule Details](Screenshot%202026-03-31%20at%2012.16.32%20PM.png)
Optimized schedule with selected and deferred tasks in priority order.

### Chronological Task View

![Chronological Order](Screenshot%202026-03-31%20at%2012.16.49%20PM.png)
Timed tasks displayed in chronological HH:MM order for easy daily planning.
