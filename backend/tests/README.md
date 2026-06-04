# Backend Automated Test Suite Documentation

To verify the reliability, safety, and correctness of the **PowerTrack** backend, a comprehensive automated test suite of **40 test cases** was implemented using **pytest**. 

The tests cover all API endpoints, data validation constraints (schemas), database operations (models), and analytical calculations (domain services).

---

## 1. Test Isolation Architecture (`conftest.py`)
To prevent tests from mutating the local production/development database (`data/fitness.db`) or interfering with each other, we implemented strict database isolation:

* **In-Memory SQLite Database**: The test configuration initializes an isolated SQLite database in-memory (`sqlite:///:memory:`) for every test session.
* **Fixture Setup & Teardown**: 
  * `db_session`: Wipes, rebuilds the schema, and starts a database transaction before running each test. Once the test finishes, the transaction is rolled back and the database is cleared.
  * `client`: Exposes a Flask test client configuration to dispatch mock HTTP requests directly to the API endpoints.

---

## 2. Test Suites Overview

The test files inside [tests/] target specific layers of the application:

###  `test_users.py` (User Management)
Verifies CRUD operations for application users and validation constraints:
* **Happy Path**: Correctly creates and retrieves users via `/users/` endpoints.
* **Validation**: Ensures attempting to register a duplicate username throws a `400 Bad Request` validation error.
* **Error Handling**: Verifies that requesting a non-existent user ID returns a `404 Not Found`.

###  `test_plans.py` (Training Plans)
Tests the schema and constraints associated with training plans:
* **Validation Limits**: Asserts that `total_weeks` must be at least 1.
* **Relationship & Ownership**: Verifies retrieval of plans by owner ID (`/plans/user/<user_id>`).
* **Cascade Deletes**: Confirms that when a user is deleted, all training plans owned by them are automatically deleted by the database cascade.

###  `test_workout_days.py` (Workout Days)
Validates the grouping of workout routines within plans:
* **Ordering Limits**: Ensures `day_order` is validated as a positive integer.
* **Orphan Cleanup**: Confirms deleting a training plan deletes all associated workout days.

###  `test_exercises.py` (Exercise Catalog)
Tests the behavior of the central exercise catalog:
* **Enumeration Constraints**: Confirms that trying to create an exercise with an invalid mechanics type (e.g. "Strength" instead of "Multi-joint", "Isolation", or "Cardio") throws a validation error.
* **Uniqueness**: Asserts that exercise names must be unique.

###  `test_plan_exercises.py` (Scheduled Exercises)
Validates scheduling exercise entities inside workout days:
* **Ordering Constraints**: Enforces that the exercise order sequence (`exercise_order`) is a positive integer.
* **Association Checks**: Checks that invalid foreign keys (e.g., adding a non-existent exercise to a day) are caught and return a `404 Not Found`.

###  `test_session_logs.py` (Workout Sessions logging)
Validates the core telemetry inputs sent by users for completed weeks:
* **Numerical Bounds**: Verifies that input values like `sets`, `reps` must be positive.
* **Load Constraints**: Checks that negative weight values (e.g., `-10 kg`) are rejected.
* **RPE Bounds**: Assures that RPE values must reside in the $[1, 10]$ range, rejecting values like `0` or `11`.

###  `test_stats.py` (Domain & Analytical Services)
Tests the core business calculations (non-anemic logic) that process raw user telemetry:
* **Volume Calculations**: Verifies correct mathematical accumulation of week-over-week training volume ($Sets \times Reps \times Weight$).
* **Filter Actions**: Checks that volume can be filtered by movement types (e.g., Compound/Multi-joint lifts only).
* **Muscle Group Balance**: Asserts that muscle load percentages are calculated correctly and sum to 100%.
* **Intensity & Recovery Reports**: Validates average RPE trends and correct filtering of logs containing physical discomfort warnings.

---

## 3.How to Run the Tests

To execute the test suite, navigate to the `backend/` directory and run:

```powershell
uv run pytest -v
```
Expected Output Summary:
```
tests/test_users.py::test_create_user PASSED
tests/test_users.py::test_duplicate_username PASSED
tests/test_plans.py::test_create_plan PASSED
tests/test_stats.py::test_volume_by_exercise PASSED
...
========================== 40 passed in 2.15s ==========================
```

