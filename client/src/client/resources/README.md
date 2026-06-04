# PowerTrack Client SDK — API Sub-Clients (`resources/`)

This package houses the resource-specific sub-client managers that make up the public namespaces of the `PowerTrackClient`. Each class exposes high-level, type-safe Python methods that wrap HTTP routing, request payload serialization, and response deserialization.

---

## Namespaces Overview

### `users.py` — UsersAPI
Exposed via `client.users`. Handles registration and deletion cascades for user profiles.
* **`list()`** $\rightarrow$ `list[User]`
* **`get(user_id)`** $\rightarrow$ `User`
* **`create(username)`** $\rightarrow$ `User`
* **`delete(user_id)`** $\rightarrow$ `dict`

---

### `plans.py` — PlansAPI
Exposed via `client.plans`. Manages training plans, which represent structured mesocycles.
* **`list()`** $\rightarrow$ `list[TrainingPlan]`
* **`get(plan_id)`** $\rightarrow$ `TrainingPlan`
* **`get_by_user(user_id)`** $\rightarrow$ `list[TrainingPlan]`
* **`create(user_id, name, total_weeks)`** $\rightarrow$ `TrainingPlan`
* **`update(plan_id, name=None, total_weeks=None)`** $\rightarrow$ `TrainingPlan`
* **`delete(plan_id)`** $\rightarrow$ `dict`

---

### `workout_days.py` — WorkoutDaysAPI
Exposed via `client.workout_days`. Manages split days (e.g. Push, Pull, Legs) scheduled inside plans.
* **`get_by_plan(plan_id)`** $\rightarrow$ `list[WorkoutDay]`
* **`get(day_id)`** $\rightarrow$ `WorkoutDay`
* **`create(plan_id, name, day_order)`** $\rightarrow$ `WorkoutDay`
* **`update(day_id, name=None, day_order=None)`** $\rightarrow$ `WorkoutDay`
* **`delete(day_id)`** $\rightarrow$ `dict`

---

### `exercises.py` — ExercisesAPI
Exposed via `client.exercises`. Manages the global catalog of physical movements.
* **`list(target_muscle=None, mechanics_type=None)`** $\rightarrow$ `list[Exercise]`
* **`get(exercise_id)`** $\rightarrow$ `Exercise`
* **`create(name, mechanics_type, target_muscle)`** $\rightarrow$ `Exercise`
* **`delete(exercise_id)`** $\rightarrow$ `dict`

---

### `plan_exercises.py` — PlanExercisesAPI
Exposed via `client.plan_exercises`. Links catalog movements to workout days with notes and ordering.
* **`get_by_day(day_id)`** $\rightarrow$ `list[PlanExercise]`
* **`get(plan_exercise_id)`** $\rightarrow$ `PlanExercise`
* **`create(workout_day_id, exercise_id, exercise_order, notes=None)`** $\rightarrow$ `PlanExercise`
* **`update(plan_exercise_id, exercise_id=None, exercise_order=None, notes=None)`** $\rightarrow$ `PlanExercise`
* **`delete(plan_exercise_id)`** $\rightarrow$ `dict`

---

### `session_logs.py` — SessionLogsAPI
Exposed via `client.session_logs`. Logs executed sets, reps, weight load, and pain reports during workout days.
* **`get_by_exercise(plan_exercise_id)`** $\rightarrow$ `list[SessionLog]`
* **`get(log_id)`** $\rightarrow$ `SessionLog`
* **`create(plan_exercise_id, week_number, sets, reps, weight, rpe=None, user_feedback=None, pain_discomfort=False)`** $\rightarrow$ `SessionLog`
* **`update(log_id, week_number=None, sets=None, reps=None, weight=None, rpe=None, user_feedback=None, pain_discomfort=None)`** $\rightarrow$ `SessionLog`
* **`delete(log_id)`** $\rightarrow$ `dict`

---

### `stats.py` — StatsAPI
Exposed via `client.stats`. Performs database aggregations and returns training volume, fatigue RPE trends, muscle volume splits, pain logs, and personal best records.
* **`get_volume_by_exercise(plan_exercise_id)`** $\rightarrow$ `ExerciseVolumeReport`
* **`get_multijoint_volume(plan_id)`** $\rightarrow$ `WeeklyVolumeReport`
* **`get_total_volume(plan_id)`** $\rightarrow$ `WeeklyVolumeReport`
* **`get_avg_rpe(plan_id)`** $\rightarrow$ `WeeklyRpeReport`
* **`get_pain_report(plan_id)`** $\rightarrow$ `PainReport`
* **`get_muscle_balance(plan_id)`** $\rightarrow$ `MuscleBalanceReport`
* **`get_personal_best(user_id, exercise_id)`** $\rightarrow$ `dict`
  *(Note: This returns a raw JSON dictionary of the personal record instead of a dataclass, ensuring dynamic serialization).*

---

## Data Model Relationship Hierarchy

The relationships between database resources are structured hierarchically:

```
User
 └── TrainingPlan
      └── WorkoutDay
           └── PlanExercise  ←── Exercise (linked global catalog)
                └── SessionLog
```

Low-level HTTP transactions (requests, JSON parsing, URL construction, and status code checks) are decoupled from these managers and handled by `BaseClient` inside `client.base`.