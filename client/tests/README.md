# PowerTrack Client SDK — Automated Test Suite

This directory contains the complete automated test suite for the **PowerTrack Python SDK**. It is built using `pytest` and implements mocking for all HTTP operations, allowing the entire suite to run offline and in milliseconds.

---

## Quick Start

To execute the test suite, ensure your virtual environment is active, navigate to the `client/` folder, and run:
```powershell
uv run pytest -v
```

Tests are discovered automatically. A running backend server or database is **not** required.

---

## Test Directory Map

Each test module maps to a corresponding component inside the source client package:

| Test File | Target Component | Description |
| :--- | :--- | :--- |
| **`conftest.py`** | Shared Fixtures | Configures the headless Matplotlib backend and defines reusable client and mock response fixtures. |
| **`test_base.py`** | `base.py`, `exceptions.py` | Validates client construction, base URL validations, context manager hooks, ping, and HTTP error response mappings. |
| **`test_users.py`** | `resources/users.py` | Verifies user creation, deletion cascade checks, listing, and single record fetching. |
| **`test_plans.py`** | `resources/plans.py` | Verifies training plan scheduling, modifications, and user filtering. |
| **`test_workout_days.py`** | `resources/workout_days.py` | Verifies day sequencing, plan binding, and split modifications. |
| **`test_exercises.py`** | `resources/exercises.py` | Verifies catalog querying, target muscle filtering, and mechanics sorting. |
| **`test_plan_exercises.py`** | `resources/plan_exercises.py` | Verifies scheduling movements onto specific splits. |
| **`test_session_logs.py`** | `resources/session_logs.py` | Verifies progressive overload entries, set/rep details, and pain report flags. |
| **`test_stats.py`** | `resources/stats.py` | Verifies analytics calculations, report parsing, and dictionary-based personal record return verification. |
| **`test_active_record.py`** | `models/` (Domain Entities) | Verifies bound entity traversals (Rich Domain Model) and unbound runtime exception protections. |
| **`test_plots.py`** | `plots/` (Visualization) | Verifies chart drawing triggers and empty dataset edge case handling. |

---

## Testing Strategy

### 1. HTTP Session Interception (`unittest.mock`)
Rather than sending actual TCP packets to `http://127.0.0.1:8000`, tests intercept HTTP calls using `unittest.mock.patch` at the `requests` level. This guarantees that:
- Tests run extremely fast (no network I/O).
- Environment setups remain deterministic.
- External database states do not affect test outcomes.

#### Mocking Example
```python
from unittest.mock import patch

def test_users_list(client, mock_response):
    # 1. Define the fake JSON body the mock server should return
    mock_response.json.return_value = [
        {"id": 1, "username": "marco"},
        {"id": 2, "username": "sara"}
    ]

    # 2. Intercept GET requests during the call
    with patch("requests.Session.get", return_value=mock_response):
        users = client.users.list()

    # 3. Verify that the SDK correctly parsed the JSON list into model instances
    assert len(users) == 2
    assert users[0].username == "marco"
```

---

### 2. Pytest Fixture Injection
Common utilities (such as initializing a fresh client or constructing a mock HTTP response) are declared in `conftest.py`. Pytest injects these objects automatically into test parameters:
```python
# conftest.py
import pytest
from unittest.mock import MagicMock
import requests
from client.client import PowerTrackClient

@pytest.fixture
def mock_response():
    response = MagicMock(spec=requests.Response)
    response.status_code = 200
    response.url = "http://127.0.0.1:8000"
    return response

@pytest.fixture
def client():
    return PowerTrackClient("http://127.0.0.1:8000")
```

---

### 3. Parametrized Exception Mappings
To test that HTTP status codes are translated to the correct Python exceptions without copying test structures, we parametrize inputs:
```python
import pytest
from client import (
    PowerTrackValidationError,
    PowerTrackNotFoundError,
    PowerTrackConflictError,
    PowerTrackServerError
)

@pytest.mark.parametrize(
    "status_code,exception_cls",
    [
        (400, PowerTrackValidationError),
        (404, PowerTrackNotFoundError),
        (409, PowerTrackConflictError),
        (500, PowerTrackServerError),
    ],
)
def test_exception_mapping(client, mock_response, status_code, exception_cls):
    mock_response.status_code = status_code
    mock_response.json.return_value = {"error": "Conflict error details"}
    
    with patch("requests.Session.get", return_value=mock_response):
        with pytest.raises(exception_cls):
            client.users.list()
```

---

### 4. Active Record Traversal Tests
We verify that entity models bound to a client successfully delegate queries. We also verify that unbound entities raise a `RuntimeError` if an active-record operation is attempted:
```python
def test_active_record_unbound_raises():
    # Constructing a model without passing a _client instance (unbound)
    user = User(id=1, username="marco")
    
    with pytest.raises(RuntimeError, match="Client not bound to this model instance"):
        user.get_plans()
```

---

### 5. Headless Plot Verification & Matplotlib Setup
The charting logic uses Matplotlib. If charts try to open a GUI window, test pipelines on headless systems (like CI environments) will fail. We configure headless execution via:

1. **`conftest.py` setup**:
   ```python
   import matplotlib
   matplotlib.use("Agg")  # Force non-interactive backend
   ```
2. **Matplotlib method mocking**: We patch `plt.show` and `plt.savefig` to verify the plotting pipeline without opening windows or creating files:
   ```python
   @patch("matplotlib.pyplot.show")
   @patch("matplotlib.pyplot.savefig")
   def test_plot_total_volume(mock_savefig, mock_show, plots, mock_client):
       mock_client.stats.get_total_volume.return_value = fake_report
       plots.plot_total_volume(plan_id=1, show=True, save_path="vol.png")
       
       mock_show.assert_called_once()
       mock_savefig.assert_called_once()
   ```