# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

These are the basic classes that I created: Owner (user profile), Pet (animal info), Task (activity details), and Scheduler (the calculation engine).

Relationship: The Owner manages the Pet, which holds a list of Tasks.

Logic: The Scheduler acts as a Controller, taking task data and a time budget to output an optimized daily plan.

- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation? Yes
- If yes, describe at least one change and why you made it.

The owner does not hold a task list, we made changes for owner to have a task list. Also there was no connection between scheduler and owner/pet so we corrected that. Also added reasons for selected tasks. Also pets needs were not linked to task selection which we added to make things easier.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

Time budget: total selected task duration must stay within the owner’s daily available minutes.

Priority: higher-priority tasks are selected first so essential care is not skipped.

Task timing conflicts: if two pet tasks are scheduled at the same HH:MM time, the system flags a warning instead of crashing.

- How did you decide which constraints mattered most?
  I deceided these mattered most by focusinf on real-world usability and pet safety first. Time and priority directly affect whether a plan is practical and whether important tasks get done.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

Scheduler chooses higher-priority tasks first within the time budget, rather than searching all possible combinations for the absolute best plan.

- Why is that tradeoff reasonable for this scenario?

## it keeps decisions fast, predictable, and focused on essential care tasks.

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
