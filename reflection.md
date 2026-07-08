# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- I designed the system using four classes: Owner, Pet, Task, and Scheduler.

- Owner stores information about the pet owner and manages their pets.
- Pet stores information about each pet and its care tasks.
- Task represents a pet care activity, including its duration, priority, and completion status.
- Scheduler is responsible for organizing tasks and generating a daily schedule based on priorities and available time.

**b. Design changes**

- After reviewing the skeleton, I noticed that Task did not store which pet it belonged to. This could make the schedule harder to display clearly later. 
- I decided to add an optional pet_name field to Task so the schedule can show which pet each task is for.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- The scheduler considers the owner's available time, each task's duration, and each task's priority. I decided that priority should matter most because important tasks like feeding, medication, or walks should be scheduled before lower-priority tasks. Available time also matters because the schedule should not include more tasks than the owner can realistically complete.

**b. Tradeoffs**

- One tradeoff is that lower-priority tasks may be skipped if there is not enough available time. This is reasonable because the scheduler should focus onv completing the most important pet care tasks first instead of trying to fit in every task.

## 3. AI Collaboration

**a. How you used AI**

- I used AI to help brainstorm the main classes, create the Mermaid UML diagram, generate the Python class skeleton, and review the design for missing relationships or possible logic issues. The AI feedback helped me notice that adding pet_name to Task would make the schedule easier to display later.

**b. Judgment and verification**

- I did not accept every AI suggestion automatically. I reviewed the feedback and only made the pet_name change because it directly helped the project goal. I verified that the UML and pawpal_system.py still matched after the change.
---

## 4. Testing and Verification

**a. What you tested**

- Now that the scheduling logic is actually implemented, I have 13 pytest tests covering the main behaviors instead of just checking that the file runs. I tested that mark_complete() flips a task's completed status and that add_task() actually adds to a pet's task list, since those are the most basic building blocks everything else depends on. I also tested sort_by_time() with three tasks added out of order (plus a case where one task has no time set, to make sure it gets pushed to the end instead of crashing or sorting weirdly). For recurrence, I tested that completing a daily task creates a new task dated exactly one day later, and a weekly one creates a task a week later, and that the new task actually ends up in the same pet's list. For conflict detection I tested both that overlapping times (and duplicate start times) get flagged, and that back-to-back tasks or tasks on different dates do NOT get flagged, since I wanted to make sure the conflict checker isn't just returning true for everything.

**b. Confidence**

- I'm fairly confident in the pieces I actually wrote tests for — sorting, filtering, recurrence, and conflict detection all pass, including the "should NOT flag this" cases, which is what makes me trust it's not just accidentally working. I'm less confident about things I haven't tested yet, like generate_schedule() when available_time is 0 or when a pet has no tasks at all, or what happens if two recurring tasks interact with the schedule on the same day. Those would be the edge cases I'd test next if I had more time.

---

## 5. Reflection

**a. What went well**

- I'm most satisfied with how the class design came together and how well the UML lines up with the actual Python skeleton. Catching the missing pet_name link on Task before writing any real logic felt like a good early win since it would've been annoying to fix after the scheduling logic was in place.

**b. What you would improve**

- If I did another iteration, I'd probably change priority from a plain string to something like an enum or a number, since sorting "high"/"medium"/"low" as strings won't actually sort in the right order. I'd also think more about how the scheduler should handle tasks that don't fit in the available time instead of just skipping them silently.

**c. Key takeaway**

- The biggest thing I learned is that it's worth reviewing AI suggestions instead of just applying all of them — the pet_name feedback was useful because it actually fixed a gap in my design, but I still had to think about whether each suggestion made sense for my project instead of just taking it at face value.
