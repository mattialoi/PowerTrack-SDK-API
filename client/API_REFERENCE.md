# PowerTrack Python Client SDK — API Reference

This document provides a comprehensive API reference for the **PowerTrack Client Library**. It covers client initialization, resource sub-clients, Active Record models, exception hierarchies, and data visualization.

---

## Table of Contents
- [PowerTrackClient (Root Client)](#powertrackclient-root-client)
- [Sub-Client Namespaces (APIs)](#sub-client-namespaces-apis)
  - [UsersAPI](#usersapi)
  - [PlansAPI](#plansapi)
  - [WorkoutDaysAPI](#workoutdaysapi)
  - [ExercisesAPI](#exercisesapi)
  - [PlanExercisesAPI](#planexercisesapi)
  - [SessionLogsAPI](#sessionlogsapi)
  - [StatsAPI](#statsapi)
- [Domain Models (Active Record)](#domain-models-active-record)
- [Exception Hierarchy](#exception-hierarchy)
- [Visualization (PowerTrackPlots)](#visualization-powertrackplots)

---

## PowerTrackClient (Root Client)

The `PowerTrackClient` class is the main entry point for the SDK. It coordinates HTTP session management, authorization, error mapping, and provides access to resource-specific sub-clients.

### Initialization
```python
from client import PowerTrackClient

# Standard initialization
client = PowerTrackClient(base_url="http://127.0.0.1:8000", timeout=10)
```

### Context Manager Support
It is highly recommended to use the client as a **Context Manager** to ensure that HTTP request sessions are properly closed:
```python
with PowerTrackClient("http://127.0.0.1:8000") as client:
    # Perform operations
    users = client.users.list()
# Connection session is automatically closed here
```

### Attributes (Sub-Clients)
- **`users`**: [`UsersAPI`](#usersapi) — User management
- **`plans`**: [`PlansAPI`](#plansapi) — Training plans
- **`workout_days`**: [`WorkoutDaysAPI`](#workoutdaysapi) — Workout days
- **`exercises`**: [`ExercisesAPI`](#exercisesapi) — Global exercise catalog
- **`plan_exercises`**: [`PlanExercisesAPI`](#planexercisesapi) — Exercise scheduling
- **`session_logs`**: [`SessionLogsAPI`](#sessionlogsapi) — Performance logging
- **`stats`**: [`StatsAPI`](#statsapi) — Training analytics & records

---

## Sub-Client Namespaces (APIs)

### UsersAPI
Exposed via `client.users`. Handles user account registration and lifecycle.

* **`list()`** $\rightarrow$ `list[User]`
  Returns all registered users in the database.
* **`get(user_id: int)`** $\rightarrow$ `User`
  Retrieves a single user by their ID. Raises `PowerTrackNotFoundError` if not found.
* **`create(username: str)`** $\rightarrow$ `User`
  Registers a new user. Raises `PowerTrackValidationError` if name is empty, or `PowerTrackConflictError` if the username is taken.
* **`delete(user_id: int)`** $\rightarrow$ `dict`
  Deletes a user and cascades deletion to all their training plans, days, logs, and statistics. Returns a status message: `{"message": "User <id> deleted"}`.

### PlansAPI
Exposed via `client.plans`. Manages training plans (workout blocks).

* **`list()`** $\rightarrow$ `list[TrainingPlan]`
  Returns all plans across all users in the system.
* **`get(plan_id: int)`** $\rightarrow$ `TrainingPlan`
  Retrieves a training plan by its ID.
* **`get_by_user(user_id: int)`** $\rightarrow$ `list[TrainingPlan]`
  Retrieves all training plans belonging to a specific user.
* **`create(user_id: int, name: str, total_weeks: int)`** $\rightarrow$ `TrainingPlan`
  Creates a plan of `total_weeks` duration for a user.
* **`update(plan_id: int, name: Optional[str] = None, total_weeks: Optional[int] = None)`** $\rightarrow$ `TrainingPlan`
  Updates a plan's name and/or duration.
* **`delete(plan_id: int)`** $\rightarrow$ `dict`
  Deletes a training plan and cascades deletion to scheduled exercises, days, and logs.

### WorkoutDaysAPI
Exposed via `client.workout_days`. Manages split days (e.g. "Push", "Pull", "Legs") inside a plan.

* **`get_by_plan(plan_id: int)`** $\rightarrow$ `list[WorkoutDay]`
  Retrieves all workout days in a plan, sorted ascending by `day_order`.
* **`get(day_id: int)`** $\rightarrow$ `WorkoutDay`
  Retrieves a single workout day.
* **`create(plan_id: int, name: str, day_order: int)`** $\rightarrow$ `WorkoutDay`
  Creates a workout day inside a plan. `day_order` is used to sort the schedule.
* **`update(day_id: int, name: Optional[str] = None, day_order: Optional[int] = None)`** $\rightarrow$ `WorkoutDay`
  Updates a day's name or ordering.
* **`delete(day_id: int)`** $\rightarrow$ `dict`
  Deletes a day and its scheduled exercises.

### ExercisesAPI
Exposed via `client.exercises`. Manages the global catalog of exercises.

* **`list(target_muscle: Optional[str] = None, mechanics_type: Optional[str] = None)`** $\rightarrow$ `list[Exercise]`
  Lists all catalog exercises, optionally filtered by target muscle (e.g., `"Chest"`, `"Legs"`) or movement type (`"Multi-joint"`, `"Isolation"`).
* **`get(exercise_id: int)`** $\rightarrow$ `Exercise`
  Retrieves a catalog exercise by its ID.
* **`create(name: str, mechanics_type: str, target_muscle: str)`** $\rightarrow$ `Exercise`
  Adds a new exercise (e.g., name="Bench Press", mechanics_type="Multi-joint", target_muscle="Chest") to the catalog.
* **`delete(exercise_id: int)`** $\rightarrow$ `dict`
  Deletes an exercise from the global catalog.

### PlanExercisesAPI
Exposed via `client.plan_exercises`. Links catalog exercises to specific workout days with ordering and notes.

* **`get_by_day(day_id: int)`** $\rightarrow$ `list[PlanExercise]`
  Retrieves scheduled exercises for a workout day, sorted ascending by `exercise_order`.
* **`get(plan_exercise_id: int)`** $\rightarrow$ `PlanExercise`
  Retrieves a single scheduled exercise entry.
* **`create(workout_day_id: int, exercise_id: int, exercise_order: int, notes: Optional[str] = None)`** $\rightarrow$ `PlanExercise`
  Schedules an exercise on a workout day.
* **`update(plan_exercise_id: int, exercise_id: Optional[int] = None, exercise_order: Optional[int] = None, notes: Optional[str] = None)`** $\rightarrow$ `PlanExercise`
  Updates a scheduled exercise's catalog reference, sorting order, or execution notes.
* **`delete(plan_exercise_id: int)`** $\rightarrow$ `dict`
  Deletes the scheduled exercise from a day.

### SessionLogsAPI
Exposed via `client.session_logs`. Records performance metrics when executing scheduled exercises.

* **`get_by_exercise(plan_exercise_id: int)`** $\rightarrow$ `list[SessionLog]`
  Retrieves all session logs for a scheduled exercise, sorted ascending by `week_number`.
* **`get(log_id: int)`** $\rightarrow$ `SessionLog`
  Retrieves a single session log by ID.
* **`create(plan_exercise_id: int, week_number: int, sets: int, reps: int, weight: float, rpe: Optional[int] = None, user_feedback: Optional[str] = None, pain_discomfort: bool = False)`** $\rightarrow$ `SessionLog`
  Logs an executed session for a given training week.
* **`update(log_id: int, ...)`** $\rightarrow$ `SessionLog`
  Updates fields of an existing session log.
* **`delete(log_id: int)`** $\rightarrow$ `dict`
  Removes a logged session.

### StatsAPI
Exposed via `client.stats`. Provides advanced analytics calculations.

* **`get_volume_by_exercise(plan_exercise_id: int)`** $\rightarrow$ `ExerciseVolumeReport`
  Returns a weekly total volume progression report for a specific scheduled exercise.
* **`get_multijoint_volume(plan_id: int)`** $\rightarrow$ `WeeklyVolumeReport`
  Calculates week-by-week total volume ($sets \times reps \times weight$) for multi-joint compound movements in a plan.
* **`get_total_volume(plan_id: int)`** $\rightarrow$ `WeeklyVolumeReport`
  Calculates week-by-week total training volume across all exercises in a plan.
* **`get_avg_rpe(plan_id: int)`** $\rightarrow$ `WeeklyRpeReport`
  Calculates the average RPE (Rate of Perceived Exertion) per week across all logged sessions.
* **`get_pain_report(plan_id: int)`** $\rightarrow$ `PainReport`
  Retrieves all sessions logged with a pain or discomfort flag, indicating weeks, exercises, and details.
* **`get_muscle_balance(plan_id: int)`** $\rightarrow$ `MuscleBalanceReport`
  Calculates volume distribution across target muscle groups (e.g. Chest, Back, Legs) as raw kg and percentage share.
* **`get_personal_best(user_id: int, exercise_id: int)`** $\rightarrow$ `dict`
  Retrieves the personal record (PR) achieved by a user for a given exercise.
  **Returns**: A Python dictionary with the following schema:
  ```python
  {
      "user_id": int,
      "exercise_id": int,
      "max_weight": float,
      "reps_at_max": int,
      "week_achieved": Optional[int]
  }
  ```

---

## Domain Models (Active Record)

All domain models are structured using Python `dataclasses`. When models are returned from the API, they are bound to the client instance (via the internal `_client` field), enabling seamless traversal of the database graph (the **Active Record** pattern).

### User
Represents a user.
- **Fields**:
  - `id`: `int` — Unique ID
  - `username`: `str` — Username
- **Active Record Methods**:
  - **`get_plans()`** $\rightarrow$ `list[TrainingPlan]`
    Shortcut for `client.plans.get_by_user(self.id)`.

### TrainingPlan
Represents a training cycle.
- **Fields**:
  - `id`: `int` — Unique ID
  - `user_id`: `int` — Owner's user ID
  - `name`: `str` — Plan name
  - `total_weeks`: `int` — Duration in weeks
  - `start_date`: `Optional[str]` — Start timestamp
- **Active Record Methods**:
  - **`get_days()`** $\rightarrow$ `list[WorkoutDay]`
    Shortcut for `client.workout_days.get_by_plan(self.id)`.
  - **`get_total_volume()`** $\rightarrow$ `WeeklyVolumeReport`
    Shortcut for `client.stats.get_total_volume(self.id)`.
  - **`get_avg_rpe()`** $\rightarrow$ `WeeklyRpeReport`
    Shortcut for `client.stats.get_avg_rpe(self.id)`.
  - **`get_pain_report()`** $\rightarrow$ `PainReport`
    Shortcut for `client.stats.get_pain_report(self.id)`.
  - **`get_muscle_balance()`** $\rightarrow$ `MuscleBalanceReport`
    Shortcut for `client.stats.get_muscle_balance(self.id)`.

### WorkoutDay
Represents a training session placeholder.
- **Fields**:
  - `id`: `int` — Unique ID
  - `plan_id`: `int` — Associated plan ID
  - `name`: `str` — Day name (e.g. "Day A - Push")
  - `day_order`: `int` — Sorting index
- **Active Record Methods**:
  - **`get_exercises()`** $\rightarrow$ `list[PlanExercise]`
    Shortcut for `client.plan_exercises.get_by_day(self.id)`.

### Exercise
Represents a cataloged exercise movement.
- **Fields**:
  - `id`: `int` — Unique ID
  - `name`: `str` — Name (e.g. "Squat")
  - `mechanics_type`: `str` — "Multi-joint" or "Isolation"
  - `target_muscle`: `str` — Target muscle group
- **Active Record Methods**:
  - **`get_personal_best(user_id: int)`** $\rightarrow$ `dict`
    Shortcut for `client.stats.get_personal_best(user_id, self.id)`. Returns a dictionary of the personal record.

### PlanExercise
Represents an exercise scheduled on a workout day.
- **Fields**:
  - `id`: `int` — Unique ID
  - `workout_day_id`: `int` — Workout day ID
  - `exercise_id`: `int` — Global catalog exercise ID
  - `exercise_order`: `int` — Sorting order index on that day
  - `notes`: `Optional[str]` — Setup notes or instructions
- **Active Record Methods**:
  - **`get_logs()`** $\rightarrow$ `list[SessionLog]`
    Shortcut for `client.session_logs.get_by_exercise(self.id)`.
  - **`get_volume_progression()`** $\rightarrow$ `ExerciseVolumeReport`
    Shortcut for `client.stats.get_volume_by_exercise(self.id)`.

### SessionLog
Represents a logged execution of an exercise.
- **Fields**:
  - `id`: `int` — Unique ID
  - `plan_exercise_id`: `int` — Scheduled exercise ID
  - `week_number`: `int` — Logged training week (1-6)
  - `sets`: `int` — Number of sets executed
  - `reps`: `int` — Reps performed per set
  - `weight`: `float` — Weight lifted in kg
  - `rpe`: `Optional[int]` — Effort intensity index (1-10)
  - `user_feedback`: `Optional[str]` — Custom training comments
  - `pain_discomfort`: `bool` — Pain/injury warning flag

---

## Exception Hierarchy

The client maps HTTP status codes returned by the REST API to structured Python exceptions. All library-specific exceptions inherit from `PowerTrackAPIError`.

```
PowerTrackAPIError (Base Client Exception)
 ├── PowerTrackValidationError (HTTP 400 - Invalid Request parameters)
 ├── PowerTrackNotFoundError    (HTTP 404 - Resource doesn't exist)
 ├── PowerTrackConflictError    (HTTP 409 - Database constraint conflicts)
 └── PowerTrackServerError      (HTTP 500 - Backend code error)
```

| Exception Class | Associated HTTP Status | Common Cause |
|---|---|---|
| `PowerTrackValidationError` | `400 Bad Request` | Creating a user with an empty username; negative weight logs. |
| `PowerTrackNotFoundError` | `404 Not Found` | Fetching a user ID that doesn't exist. |
| `PowerTrackConflictError` | `409 Conflict` | Creating duplicate username; scheduling duplicate exercises on a day. |
| `PowerTrackServerError` | `500 Internal Error` | Database connection lost; unhandled server exceptions. |

---

## Visualization (PowerTrackPlots)

`PowerTrackPlots` acts as the visualization interface, plotting matplotlib graphs of training statistics. It takes a `PowerTrackClient` instance as a parameter.

### Methods
Each method accepts a `show` flag (displays the chart window if `True`) and a `save_path` string (saves the chart to disk as a `.png` file if provided).

* **`plot_volume_progression(plan_exercise_id: int, show: bool = True, save_path: Optional[str] = None)`**
  Plots a line chart of the week-by-week volume progression and a dashed secondary-axis trend of RPE ratings.
* **`plot_total_volume(plan_id: int, show: bool = True, save_path: Optional[str] = None)`**
  Plots a bar chart showing the total tonnage lifted ($sets \times reps \times weight$) during each week of a training plan.
* **`plot_multijoint_vs_total(plan_id: int, show: bool = True, save_path: Optional[str] = None)`**
  Plots an overlapping bar chart displaying total weekly volume vs. multi-joint compound movement volume, illustrating program selection balance.
* **`plot_rpe_trend(plan_id: int, show: bool = True, save_path: Optional[str] = None)`**
  Plots a weekly average RPE trend line, helping visualize fatigue buildup and overall training stress.
* **`plot_muscle_balance(plan_id: int, show: bool = True, save_path: Optional[str] = None)`**
  Plots a horizontal bar chart breaking down training volume distribution across targeted muscle groups.
* **`plot_pain_report(plan_id: int, show: bool = True, save_path: Optional[str] = None)`**
  Plots a scatter and bar timeline of logged sessions flagged with pain or discomfort, aiding injury tracking.
