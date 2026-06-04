# PowerTrack Client SDK — Domain Models & Active Record

This package contains the typed Python `dataclass` models that represent API resources. By binding a backreference of the client to each model instance, the SDK implements the **Active Record** pattern. This allows developers to query relationships and fetch analytics directly from the objects themselves.

---

## The Active Record Pattern

Normally, fetching data requires passing IDs to a client service:
```python
# Standard service call:
plans = client.plans.get_by_user(user_id=1)
```

With the **Active Record** pattern, models carry their own context. You can traverse the training graph directly:
```python
# Active Record traversal:
user = client.users.get(1)
plans = user.get_plans()  # Fetches plans for this user instance automatically
```

Circular references between models (e.g. `User` referencing `TrainingPlan`, which references `WorkoutDay`) are resolved using the `TYPE_CHECKING` guard combined with string forward declarations, preventing imports at execution runtime.

---

## Entity Models

### User
Represents a registered user on the platform.
* **Namespace**: `client.models.User`

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | `int` | Unique database user ID |
| `username` | `str` | Registered username (unique) |

#### Relationships & Methods
* **`get_plans()`** $\rightarrow$ `list[TrainingPlan]`
  Returns all training plans belonging to this user.

---

### TrainingPlan
Represents a block of training weeks (e.g. a mesocycle).
* **Namespace**: `client.models.TrainingPlan`

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | `int` | Unique plan ID |
| `user_id` | `int` | ID of the user who owns this plan |
| `name` | `str` | Name of the plan (e.g. "Hypertrophy Block A") |
| `total_weeks` | `int` | Plan duration in weeks |
| `start_date` | `Optional[str]` | Timestamp when the plan was initialized |

#### Relationships & Methods
* **`get_days()`** $\rightarrow$ `list[WorkoutDay]`
  Returns all split days associated with the plan, sorted by order.
* **`get_total_volume()`** $\rightarrow$ `WeeklyVolumeReport`
  Calculates week-by-week total tonnage lifted.
* **`get_avg_rpe()`** $\rightarrow$ `WeeklyRpeReport`
  Calculates week-by-week average RPE ratings.
* **`get_pain_report()`** $\rightarrow$ `PainReport`
  Lists all sessions that reported pain or discomfort.
* **`get_muscle_balance()`** $\rightarrow$ `MuscleBalanceReport`
  Calculates total training tonnage split by target muscle group.

---

### WorkoutDay
Represents a split day within a plan.
* **Namespace**: `client.models.WorkoutDay`

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | `int` | Unique day ID |
| `plan_id` | `int` | Parent plan ID |
| `name` | `str` | Day name (e.g., "Leg Day B") |
| `day_order` | `int` | Sorting index of the day (e.g. `1` for Monday) |

#### Relationships & Methods
* **`get_exercises()`** $\rightarrow$ `list[PlanExercise]`
  Returns exercises scheduled for this day, sorted ascending by order.

---

### Exercise
Represents a movement catalog entry.
* **Namespace**: `client.models.Exercise`

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | `int` | Unique catalog exercise ID |
| `name` | `str` | Display name (e.g. "Overhead Press") |
| `mechanics_type` | `str` | `"Multi-joint"` or `"Isolation"` |
| `target_muscle` | `str` | Target muscle group (e.g. `"Shoulders"`) |

#### Relationships & Methods
* **`get_personal_best(user_id: int)`** $\rightarrow$ `dict`
  Fetches the user's personal record for this exercise.
  **Returns**: A dictionary containing `max_weight`, `reps_at_max`, and `week_achieved`.

---

### PlanExercise
Represents a catalog exercise scheduled on a workout day.
* **Namespace**: `client.models.PlanExercise`

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | `int` | Unique scheduled exercise ID |
| `workout_day_id` | `int` | Associated workout day ID |
| `exercise_id` | `int` | Associated catalog exercise ID |
| `exercise_order` | `int` | Sorting index on the day's exercise list |
| `notes` | `Optional[str]` | Optional execution tips or cues |

#### Relationships & Methods
* **`get_logs()`** $\rightarrow$ `list[SessionLog]`
  Returns performance session logs recorded for this scheduled exercise, ordered by week.
* **`get_volume_progression()`** $\rightarrow$ `ExerciseVolumeReport`
  Returns weekly volume tonnage and intensity metrics for this exercise.

---

### SessionLog
Represents performance data recorded for a scheduled exercise.
* **Namespace**: `client.models.SessionLog`

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | `int` | Unique log ID |
| `plan_exercise_id` | `int` | Associated scheduled exercise ID |
| `week_number` | `int` | Week of training when log was recorded (e.g. `4`) |
| `sets` | `int` | Sets performed |
| `reps` | `int` | Reps performed per set |
| `weight` | `float` | Load lifted in kilograms (kg) |
| `rpe` | `Optional[int]` | Rating of Perceived Exertion (1 to 10 scale) |
| `user_feedback` | `Optional[str]` | Free-form training feedback or notes |
| `pain_discomfort` | `bool` | Injury warning flag |

---

## Analytics Report Models (`stats_reports.py`)

These plain data dataclasses deserialize stats responses returned from API operations:

1. **`ExerciseVolumeReport`**: Volume progression for a single exercise.
   * `plan_exercise_id: int`
   * `exercise: str`
   * `data: list[ExerciseVolumeData]` (each containing `week_number`, `sets`, `reps`, `weight`, `volume`, `rpe`).
2. **`WeeklyVolumeReport`**: Weekly tonnage report.
   * `plan_id: int`
   * `mechanics_type: Optional[str]`
   * `data: list[WeeklyVolumeData]` (each containing `week_number`, `total_volume`).
3. **`WeeklyRpeReport`**: Average Weekly intensity report.
   * `plan_id: int`
   * `data: list[WeeklyRpeData]` (each containing `week_number`, `avg_rpe`, `sessions_logged`).
4. **`PainReport`**: Discomfort tracking.
   * `plan_id: int`
   * `total_pain_flags: int`
   * `data: list[PainLog]` (each containing `week_number`, `exercise`, `rpe`, `user_feedback`).
5. **`MuscleBalanceReport`**: Muscle group balance.
   * `plan_id: int`
   * `total_volume: float`
   * `data: list[MuscleBalanceData]` (each containing `target_muscle`, `total_volume`, `percentage`).

---

## Circular Imports Mitigation

Because domain entities reference each other, importing them directly would create cyclic execution errors. We resolve this using:

### 1. `TYPE_CHECKING` guards
Imports are only loaded during code validation (by analysis tools/IDEs) and are never executed at runtime:
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from client.models.plan import TrainingPlan
```

### 2. Quoted Forward References
Since type hints are not resolved at runtime, models refer to each other using string representations:
```python
def get_plans(self) -> list["TrainingPlan"]:
    # "TrainingPlan" is wrapped as a string
```