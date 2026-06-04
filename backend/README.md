# PowerTrack Backend Web Service

This is the Flask-based REST web service for **PowerTrack**, a workout tracking and training analytics application. It provides CRUD operations for users, plans, and session logs, alongside domain-specific services for training volume, effort intensity, and recovery reports.

---

## Architectural Design

The backend is built around a modern, modular layered architecture that decouples database access from HTTP route presentation and domain business logic, avoiding an **Anemic Domain Model** (where data models are dumb schemas and routes hold all logic).

```
                  ┌───────────────────────┐
                  │      HTTP Clients     │
                  └───────────┬───────────┘
                              │ JSON
                              ▼
                  ┌───────────────────────┐
                  │    Blueprints/Routes  │
                  └───────────┬───────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
          ┌───────────────────┐ ┌───────────────┐
          │  Domain Services  │ │ Marshmallow   │ (Data Validation
          └─────────┬─────────┘ │    Schemas    │  & Serialization)
                    │           └───────────────┘
                    ▼
          ┌───────────────────┐
          │  SQLAlchemy ORM   │ (Database Layer)
          │      Models       │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │  SQLite Database  │
          └───────────────────┘
```

The app is organized into the following directories:
* **[app/models/]**: SQLAlchemy ORM database models specifying table schemas and constraints.
* **[app/routes/]**: Flask blueprints handling HTTP routing, input parsing, and JSON replies.
* **[app/schemas/]**: Marshmallow schemas for validating API inputs and serialization formatting.
* **[app/services/]**: Encapsulates database CRUD operations and advanced training domain calculations.
* **[tests/]**: Automated unit and integration test suite executing on isolated in-memory DB setups.

---

## Getting Started

### 1. Environment Setup
Every time you open a new PowerShell terminal, run these commands to activate the virtual environment  (in \backend):

```powershell
# 0. sync the venv (only the first time)
uv sync 
uv run python -m app.main
# 1. Activate the virtual environment
.venv\Scripts\Activate.ps1

# 2. Tell Flask where the application entry point is
$env:FLASK_APP = "app.main:create_app"

# 3. Enable development mode (optional, enables auto-reload and debug trace)
#$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"
```

### 2. Run the Server
Launch the REST API on port 8000 (recommended):

```powershell
uv run python -m app.main
```
Verify the server is running by opening [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser. You should receive:
```json
{"message": "PowerTrack API online", "status": 200}
```

### 3. Open Flask Shell
To inspect state or test operations interactively, set the Python path to the current directory and open the shell:
```powershell
# Set PYTHONPATH so absolute imports resolve correctly
$env:PYTHONPATH = "."
uv run flask --app app.main:create_app shell
```
Inside the interactive shell:
```python
from backend.app.database import db
from backend.app.models.user import User

# Query all users
User.query.all()
```

---

## Testing

The backend includes a comprehensive pytest suite (40 test cases) ensuring correct functionality of all endpoints, validation constraints, and business analytics.

Tests run against a temporary, isolated **in-memory SQLite database** (`sqlite:///:memory:`), which is wiped and rebuilt for each test function to guarantee no side effects between tests.

To run the test suite:
```powershell
python pytest -v
```

---

## Sub-Module Documentation

For specific information on how individual components are structured, check the dedicated sub-folder documentations:
1. [Models README (Database Schema)](app/models/README.md)
2. [Routes README (HTTP Endpoints)](app/routes/README.md)
3. [Schemas README (Data Validation)](app/schemas/README.md)
4. [Services README (Domain Logic)](app/services/README.md)
5. [Tests README (Backend tests)](tests/README.md)

---

## Project Requirements Checklist 

* **- REST Web Service API**: Implemented using Flask Blueprints mapping clean endpoints `/users/`, `/plans/`, `/workout-days/`, `/exercises/`, `/plan-exercises/`, `/session-logs/`, and `/stats/` supporting standard HTTP methods (`GET`, `POST`, `PUT`, `DELETE`).
* **- Relational Database Storage**: Utilizes SQLite with Flask-SQLAlchemy ORM. Database schemas and relationships are defined dynamically under `app/models/` with foreign keys and cascade deletions enabled.
* **- Decoupling Architecture**: Complete separation of concerns. HTTP routes (`app/routes/`) only parse requests and format responses; database querying and business logic are fully decoupled into the service layer (`app/services/`).
* **- Non-Anemic Domain Model**: Business rules and mathematical domain calculations (weekly volume, compound lift volume split, muscle balance, RPE intensity logs, and pain recovery flags) are implemented in domain services (`volume.py`, `intensity.py`, `recovery.py`, `personal_bests.py`) rather than leaving entities as simple data-less models.
* **- Robust Input Validation**: Employs Marshmallow schemas (`app/schemas/`) validating types, values (e.g. positive bounds for reps/sets, RPE range validation $[1, 10]$, Mechanics enum validation), and discarding non-permitted payload injections using `dump_only=True`.
* **- Automated Unit & Integration Tests**: 40 unit and integration tests written in `tests/` leveraging `pytest`. Complete environment isolation is implemented using an in-memory SQLite database (`sqlite:///:memory:`) with setup and rollback operations per test (in `conftest.py`).