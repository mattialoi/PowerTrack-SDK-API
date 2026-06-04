# PowerTrack Client Library SDK

Welcome to the Python client library for **PowerTrack**, a full-stack workout tracking and training analytics platform. This SDK hides all HTTP/JSON transport details from the caller, mapping backend REST endpoints to clean, object-oriented Python interfaces using the **Active Record** domain model pattern.

---

## Architectural Design

The SDK is organized as a modular, layered library that separates HTTP transport, exception translation, domain model structures, and data visualization.

```
                  ┌───────────────────────┐
                  │       Caller Code     │
                  └───────────┬───────────┘
                              │ Programmatic Python Calls
                              ▼
                  ┌───────────────────────┐
                  │    PowerTrackClient   │  (client.py)
                  │   + sub-clients on    │
                  │   .users .plans ...   │
                  └───────────┬───────────┘
                              │
                    ┌─────────┴──────────┐
                    ▼                    ▼
          ┌──────────────────┐  ┌─────────────────────┐
          │  Resource APIs   │  │   PowerTrackPlots   │
          │  (resources/)    │  │     (plots/)        │
          └────────┬─────────┘  └─────────────────────┘
                   │
                   ▼
          ┌──────────────────┐
          │   BaseClient     │  (base.py)
          │  HTTP transport  │
          │  + error mapping │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │  Dataclass       │
          │  Models          │  (models/)
          │  + active record │
          └──────────────────┘
```

### Namespace & Folder Structure
- **[`src/client/resources/`](src/client/resources/)**: Exposes one sub-client class per API resource domain (`users`, `plans`, `workout_days`, `exercises`, `plan_exercises`, `session_logs`, and `stats`).
- **[`src/client/models/`](src/client/models/)**: Houses typing-enforced `dataclasses` that represent API schemas, equipped with **Active Record** convenience methods.
- **[`src/client/plots/`](src/client/plots/)**: Chart generation mixins that render training progress graphs (volume, intensity, recovery) using matplotlib.
- **[`base.py`](src/client/base.py)**: Low-level REST transport client that manages the `requests.Session` pool, translates HTTP status codes into typed python exceptions, and implements context manager hooks.
- **[`exceptions.py`](src/client/exceptions.py)**: A structured custom exception hierarchy derived from `PowerTrackAPIError`.

---

## Getting Started

### 1. Environment Sync
Ensure you are using Python 3.12+ and have `uv` installed. Set up your virtual environment in the `client/` folder:
```powershell
# Sync venv dependencies
uv sync

# Activate the environment (Windows PowerShell)
.venv\Scripts\Activate.ps1
```

### 2. Build and Install the Wheel
During integration or deployment, you can build the client library into a redistributable wheel package:
```powershell
# Build wheel file under client/dist/
uv build

# Install the wheel in your python environment
pip install dist/client-0.1.0-py3-none-any.whl
```
Alternatively, for active local development, install in editable mode:
```powershell
pip install -e .
```

### 3. Quickstart Example
```python
from client import PowerTrackClient

# Initialize using context manager to ensure connection reuse & cleanup
with PowerTrackClient("http://127.0.0.1:8000") as client:
    # 1. Register a user
    user = client.users.create(username="marco")
    print(f"Registered user: {user.username} (ID: {user.id})")
    
    # 2. Create a training plan
    plan = client.plans.create(user_id=user.id, name="Strength Block A", total_weeks=6)
    
    # 3. Use Active Record methods to traverse relationships directly
    plans = user.get_plans()
    print(f"User plans: {[p.name for p in plans]}")
```

---

## SDK Features

### API Sub-Clients
Low-level operations are routed via dedicated resource namespaces. All methods return structured models:

| Sub-client Namespace | Access Attribute | Key Operations |
|---|---|---|
| `UsersAPI` | `client.users` | `list`, `get`, `create`, `delete` |
| `PlansAPI` | `client.plans` | `list`, `get`, `get_by_user`, `create`, `update`, `delete` |
| `WorkoutDaysAPI` | `client.workout_days` | `get_by_plan`, `get`, `create`, `update`, `delete` |
| `ExercisesAPI` | `client.exercises` | `list`, `get`, `create`, `delete` |
| `PlanExercisesAPI` | `client.plan_exercises` | `get_by_day`, `get`, `create`, `update`, `delete` |
| `SessionLogsAPI` | `client.session_logs` | `get_by_exercise`, `get`, `create`, `update`, `delete` |
| `StatsAPI` | `client.stats` | `get_volume_by_exercise`, `get_multijoint_volume`, `get_total_volume`, `get_avg_rpe`, `get_pain_report`, `get_muscle_balance`, `get_personal_best` |

### Active Record Models
Dataclasses represent the business entities. Models are initialized with a backreference to the client, allowing you to trigger actions directly from the instance:
```python
# Instead of calling client.stats.get_total_volume(plan.id):
volume_report = plan.get_total_volume()
```
For a list of all model fields and Active Record shortcuts, see [Models Documentation](src/client/models/README.md).

### Training Data Visualization
`PowerTrackPlots` provides data visualization capabilities. It runs query requests behind the scenes and plots charts directly:
```python
from client import PowerTrackClient, PowerTrackPlots

with PowerTrackClient("http://127.0.0.1:8000") as client:
    plots = PowerTrackPlots(client)
    
    # Generate and save charts to disk
    plots.plot_total_volume(plan_id=1, save_path="total_volume.png")
    plots.plot_rpe_trend(plan_id=1, save_path="rpe_trend.png")
```

### Exception Mapping
HTTP 4xx and 5xx errors are caught at the transport layer and raised as typed Python exceptions:
- `PowerTrackValidationError` (400 Bad Request)
- `PowerTrackNotFoundError` (404 Not Found)
- `PowerTrackConflictError` (409 Conflict)
- `PowerTrackServerError` (500 Server Error)

---

## API Reference & Guides

For complete method signatures, type hints, active-record definitions, and plotter configuration details, refer to:
1. **[API Reference Guide](API_REFERENCE.md)**
2. **[Domain Models Guide](src/client/models/README.md)**
3. **[Sub-Client resources Guide](src/client/resources/README.md)**
4. **[Test Suite Documentation](tests/README.md)**

---

## Testing

Execute the automated test suite locally to verify code changes:
```powershell
uv run pytest -v
```
All HTTP communication is intercepted and mocked inside the test suite, allowing it to run offline without a live server instance.

---

## API Reference & Guides

For specific information on how individual components are structured, check the dedicated sub-folder documentations:
1. [API Reference (API Guide)](API_REFERENCE.md)
2. [Models (Domain Models Guide)](src/client/models/README.md)
3. [resources (Sub-Client resources Guide)](src/client/resources/README.md)
4. [Test (Client Tests)](tests/README.md)

---


## Client Library Requirements Fulfillment

This Python package allows developers to interact with the web service programmatically. Below is the checklist mapping how each requirement was satisfied:

### API Wrapper
- **One method per exposed backend operation** (mirrors all CRUD and advanced endpoints)
  * Implemented inside `client.users`, `client.plans`, `client.workout_days`, `client.exercises`, `client.plan_exercises`, `client.session_logs`, and `client.stats` (refer to the [API Reference Guide](API_REFERENCE.md) for method names).
- **Clean, intuitive interface** — hides HTTP details from the caller
  * Low-level concerns (like request construction, payload validation, URLs, and JSON serialization) are hidden in `BaseClient`. Developers interact solely with typed dataclasses and standard python types (e.g. `dict` returns for personal records).
- **Proper error handling** (HTTP errors, connection issues, unexpected responses)
  * Translates HTTP errors (400, 404, 409, 500) into subclassed exceptions of `PowerTrackAPIError` at the transport layer (`BaseClient._raise_for_error()`).

### Data Visualisation
- **At least one plot or diagram generated** from data returned by the web service
  * Generates 6 different visual plots (progression lines, workload tonnage bars, multi-joint splits, RPE scatter trends, muscle distribution pie charts, and physical discomfort timelines).
- **Use a plotting library** such as `matplotlib`
  * Fully implemented inside `PowerTrackPlots` utilizing `matplotlib.pyplot`.

### Code Quality
- **Object-oriented design** — class-based structure
  * Built using class modules including `BaseClient`, `PowerTrackClient`, sub-clients (`UsersAPI`, etc.), domain models (`User`, etc.), and plotting mixins (`VolumePlotterMixin`, etc.).
- **Virtual environment managed** with `uv`
  * Workspace packages and dependencies (like `matplotlib` and `pytest`) are locked and managed with `uv.lock` and `pyproject.toml`.
- **Full unit test coverage** — use mocks for HTTP calls
  * Contains 57 unit tests mock-intercepting `requests.Session` methods to guarantee fast, deterministic, offline execution.
- **Built and distributed as a wheel package** (`.whl`)
  - `pyproject.toml` correctly configured with `hatchling` as the build system.
  - Package installable via `pip install client-0.1.0-py3-none-any.whl`.
