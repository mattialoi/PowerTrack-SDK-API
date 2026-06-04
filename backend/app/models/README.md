# Database Models & Schema (SQLAlchemy ORM)

This package contains the **SQLAlchemy ORM Models** representing the database schema for the PowerTrack application. The models define the structure of the database tables, field constraints, and relationships.

---

## Database Schema Entity-Relationship Map


```text
  ┌───────────────────┐
  │       USER        │
  ├───────────────────┤
  │ PK │ id           │
  │    │ username     │
  └─────────┬─────────┘
            │ 1
            │
            │ ──┐ (Has many)
            ▼   │ N
  ┌─────────────┴─────┐
  │   TRAINING_PLAN   │
  ├───────────────────┤
  │ PK │ id           │
  │ FK │ user_id      │
  │    │ name         │
  │    │ total_weeks  │
  │    │ start_date   │
  └─────────┬─────────┘
            │ 1
            │
            │ ──┐ (Contains)
            ▼   │ N
  ┌─────────────┴─────┐
  │    WORKOUT_DAY    │
  ├───────────────────┤
  │ PK │ id           │
  │ FK │ plan_id      │
  │    │ name         │
  │    │ day_order    │
  └─────────┬─────────┘
            │ 1
            │
            │ ──┐ (Schedules)              ┌────────────────────┐
            ▼   │ N                        │      EXERCISE      │
  ┌─────────────┴──────┐                   ├────────────────────┤
  │   PLAN_EXERCISE    │ N               1 │ PK │ id            │
  ├────────────────────┼───────────────────┤    │ name          │
  │ PK │ id            │                   │    │ mechanics_type│
  │ FK │ workout_day_id│                   │    │ target_muscle │
  │ FK │ exercise_id   │                   └────────────────────┘
  │    │ exercise_order│
  │    │ notes         │
  └─────────┬──────────┘
            │ 1
            │
            │ ──┐ (Logs)
            ▼   │ N
  ┌─────────────┴─────┐
  │    SESSION_LOG    │
  ├───────────────────┤
  │ PK │ id           │
  │ FK │ plan_ex_id   │
  │    │ week_number  │
  │    │ sets         │
  │    │ reps         │
  │    │ weight       │
  │    │ rpe          │
  │    │ user_feedback│
  │    │ pain_discomf │
  └───────────────────┘
```

---

## Entities & Fields Description

### 1. `User` (`users` table)
Represents a registered user in the application.
- `id` (Integer, Primary Key): Unique identifier.
- `username` (String(50), Unique, Nullable=False): The unique name of the user.
- **Relationships**: One-to-Many with `TrainingPlan` (`backref="user"`, cascade delete enabled).

### 2. `TrainingPlan` (`training_plans` table)
Represents a multi-week physical training plan designed for a user.
- `id` (Integer, Primary Key): Unique identifier.
- `user_id` (Integer, Foreign Key `users.id`): Owner of the plan.
- `name` (String(100), Nullable=False): The title of the training program.
- `total_weeks` (Integer, Nullable=False): Duration of the training plan in weeks.
- `start_date` (DateTime, Default=UTC Now): Day on which the plan was initialized.
- **Relationships**: One-to-Many with `WorkoutDay` (`backref="plan"`, cascade delete enabled).

### 3. `WorkoutDay` (`workout_days` table)
Represents a specific day of training within a weekly cycle (e.g., "Day 1: Upper Body", "Day 2: Lower Body").
- `id` (Integer, Primary Key): Unique identifier.
- `plan_id` (Integer, Foreign Key `training_plans.id`): Parent plan this day belongs to.
- `name` (String(100), Nullable=False): Description of the workout day.
- `day_order` (Integer, Nullable=False): Execution order of the day within the week (e.g. 1st day, 2nd day).
- **Relationships**: One-to-Many with `PlanExercise` (`backref="workout_day"`, cascade delete enabled).

### 4. `Exercise` (`exercises` table)
A catalog of available movements (e.g., "Squat", "Bench Press") containing global properties.
- `id` (Integer, Primary Key): Unique identifier.
- `name` (String(100), Unique, Nullable=False): The name of the exercise.
- `mechanics_type` (String(50), Nullable=False): Type of movement (`Multi-joint`, `Isolation`, or `Cardio`).
- `target_muscle` (String(100), Nullable=False): The primary muscle worked (e.g., `Chest`, `Quads`, `Lats`).

### 5. `PlanExercise` (`plan_exercises` table)
An association table connecting `WorkoutDay` and `Exercise`, scheduling an exercise to be done on a specific day.
- `id` (Integer, Primary Key): Unique identifier.
- `workout_day_id` (Integer, Foreign Key `workout_days.id`): Associated workout day.
- `exercise_id` (Integer, Foreign Key `exercises.id`): Reference to the catalog exercise.
- `exercise_order` (Integer, Nullable=False): Execution sequence of the exercise during the workout.
- `notes` (Text, Nullable=True): Setup or instruction notes (e.g. "Tempo 3-1-1").
- **Relationships**: One-to-Many with `SessionLog` (`backref="plan_exercise"`, cascade delete enabled).

### 6. `SessionLog` (`session_logs` table)
The actual historical execution log for a specific exercise in a given week.
- `id` (Integer, Primary Key): Unique identifier.
- `plan_exercise_id` (Integer, Foreign Key `plan_exercises.id`): Reference to the scheduled exercise.
- `week_number` (Integer, Nullable=False): The week index when the workout occurred.
- `sets` (Integer, Nullable=False): Number of sets completed.
- `reps` (Integer, Nullable=False): Number of reps per set.
- `weight` (Float, Nullable=False): Load lifted in kilograms.
- `rpe` (Integer, Nullable=True): Rating of Perceived Exertion (1 to 10 scale).
- `user_feedback` (Text, Nullable=True): Arbitrary notes on feelings or execution.
- `pain_discomfort` (Boolean, Default=False): Indication of joint or muscle pain during execution.
