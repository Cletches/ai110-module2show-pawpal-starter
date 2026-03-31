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

I used AI in designing, debugging and running test and edge cases

- What kinds of prompts or questions were most helpful?

I think the most helpful prompts were when I was very specific on the file it should use and things to conside

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

It suggested a complex algorithm in one of my implementations so I neglected and used a simpler one

- How did you evaluate or verify what the AI suggested?

## I verified by testing to see if it works. I also viewed code to make sure I understood what the code was about

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

Some cases passed and others did not. So I went back to correct cases where tests did not pass

- Why were these tests important?

Tests are important to make sure everything works smoothly. Without test, we can ship code that will break

**b. Confidence**

- How confident are you that your scheduler works correctly?

I am very confident 5/5. since most tests passed

- What edge cases would you test next if you had more time?

I did one thing was I could customize my own pet to add. I was limited to the pets to select from

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I really like the UI. It was very simple and user friendly

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

Maybe I could add more features to enable users have more flexibility

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Initial designs could change as time goes on. I started with a simple UML diagram and ended with a different UML

Which Copilot features were most effective for building your scheduler?

Generating test cases and edge cases

How did using separate chat sessions for different phases help you stay organized?

It helped the AI to focus more on the current task

Summarize what you learned about being the "lead architect" when collaborating with powerful AI tools.

It was very good and useful tool, especially in getting the UML diagram after many changes were made.
