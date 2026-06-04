# Domain Services (Business Logic)

This package contains the core business logic of the PowerTrack application, keeping the database layer decoupled from the presentation layer (Blueprints).

---

## Architectural Patterns

Services are structured into two categories:

### 1. Database CRUD Services
These services manage database transactions and integrity checks:
- `user_service.py`
- `exercise_service.py`
- `plan_service.py`
- `workout_day_service.py`
- `plan_exercise_service.py`
- `session_log_service.py`

### 2. Domain-Oriented Analytics Services
These services contain the core mathematical and logical formulas of the training domain, avoiding an Anemic Domain Model:
- **`volume.py`**: Calculates sets x reps x load weekly volume statistics, aggregates plan logs, and computes muscle group balance.
- **`intensity.py`**: Processes Rating of Perceived Exertion (RPE) logs to track fatigue thresholds.
- **`recovery.py`**: Compiles pain report lists to flag injury risks.
- **`personal_bests.py`**: Queries all training history to retrieve maximum weight lifted per exercise for a user.