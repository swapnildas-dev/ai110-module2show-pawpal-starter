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

- Right now I haven't actually tested any behaviors yet because generate_schedule(), sort_tasks(), and the other methods are still just stubs with pass — there's no real logic to run. The only thing I've "tested" so far is making sure the classes actually match the UML and that the file runs without errors.

**b. Confidence**

- I can't say I'm confident the scheduler works correctly since none of the scheduling logic exists yet — that part is still ahead of me. Once I implement it, I'd want to test edge cases like available_time being 0, a pet with no tasks, multiple tasks with the same priority, and a Task with pet_name left as None to make sure display_schedule() doesn't break.

---

## 5. Reflection

**a. What went well**

- I'm most satisfied with how the class design came together and how well the UML lines up with the actual Python skeleton. Catching the missing pet_name link on Task before writing any real logic felt like a good early win since it would've been annoying to fix after the scheduling logic was in place.

**b. What you would improve**

- If I did another iteration, I'd probably change priority from a plain string to something like an enum or a number, since sorting "high"/"medium"/"low" as strings won't actually sort in the right order. I'd also think more about how the scheduler should handle tasks that don't fit in the available time instead of just skipping them silently.

**c. Key takeaway**

- The biggest thing I learned is that it's worth reviewing AI suggestions instead of just applying all of them — the pet_name feedback was useful because it actually fixed a gap in my design, but I still had to think about whether each suggestion made sense for my project instead of just taking it at face value.
