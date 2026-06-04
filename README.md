# PowerTrack — Fitness & Training Analytics Platform

PowerTrack is a full-stack training tracker and analytics platform. Developed as a laboratory project for the Data Science and Artificial Intelligence curriculum at SUPSI, it consists of three independent components managed inside a single monorepo:

1. **Flask REST Backend**: A structured HTTP REST API backed by a SQLite database using Flask-SQLAlchemy, with validation Marshmallow schemas.
2. **Python Client Library SDK**: A programmatic Python library packaged as a wheel (`.whl`). It implements the Active Record pattern, exception translation, and Matplotlib visualizations.
3. **Demo Client**: Interactive command-line and Jupyter Notebook clients that install the compiled SDK wheel and simulate a six-week progressive overload training lifecycle.

---

## Repository Map

```
group-13-loi-falcao/
│
├── backend/                    # Flask REST Web Service
│   ├── app/
│   │   ├── models/             # SQLAlchemy ORM schemas
│   │   ├── routes/             # Blueprints (HTTP controller endpoints)
│   │   ├── schemas/            # Marshmallow request/response serializers
│   │   └── services/           # Database CRUD & analytics calculations
│   ├── tests/                  # Backend pytest suite (40 tests)
│   ├── pyproject.toml          # Backend package config
│   └── README.md               # Backend docs -> backend/README.md
│
├── client/                     # Python Client SDK Library
│   ├── src/client/
│   │   ├── models/             # Dataclass models (Active Record convenience methods)
│   │   ├── resources/          # API sub-clients (users, plans, stats, etc.)
│   │   └── plots/              # Matplotlib chart generators
│   ├── tests/                  # Client pytest suite (57 tests, mocked network)
│   ├── pyproject.toml          # Packaging metadata (uv_build backend)
│   ├── API_REFERENCE.md        # Comprehensive SDK reference -> client/API_REFERENCE.md
│   └── README.md               # SDK client docs -> client/README.md
│
├── demo/                       # Demonstration Application
│   ├── demo.py                 # Interactive CLI client
│   ├── example_usage.ipynb     # Jupyter Notebook (inline analytics charts)
│   ├── charts/                 # Generated PNG training report plots
│   ├── pyproject.toml          # Demo workspace package configuration
│   └── README.md               # Demo docs -> demo/README.md
│
├── data/
│   └── fitness.db              # SQLite Database (auto-generated on first app launch)
│
├── .gitignore
├── Project requirements.md     # Project design specification list
└── README.md                   # Root documentation (this file)
```

---

## Quick Start Setup

Each workspace folder manages its virtual environment independently using **`uv`**. Follow these instructions in order:

### Step 1: Launch the Backend
Open a terminal, go to the `backend/` directory, sync dependencies, and start the server:
```powershell
cd backend
uv sync
uv run python -m app.main
```
The server will boot on `http://127.0.0.1:8000/`. Visit this URL in your browser to verify connectivity. See [backend/README.md](backend/README.md) for details.

### Step 2: Compile the Client Library Wheel
Open a new terminal, go to the `client/` directory, sync package metadata, and compile:
```powershell
cd client
uv sync
uv build
```
This packages the SDK into `client/dist/client-0.1.0-py3-none-any.whl`. For method declarations, check [client/README.md](client/README.md) and the [API Reference Guide](client/API_REFERENCE.md).

### Step 3: Run the Demonstration Cycle
Go to the `demo/` directory, sync (which installs the local compiled client wheel automatically), and run:
```powershell
cd demo
uv sync
uv run python demo.py
```
To run the interactive notebook instead, launch:
```powershell
uv run jupyter notebook
```
Then open `example_usage.ipynb`. See [demo/README.md](demo/README.md) for execution details.

---

## Running the Unit Tests

Automated testing is configured for both the backend and client.

### Backend Tests (40 tests)
Verifies HTTP endpoints, serialization validation limits, cascades, and calculations using a sandboxed in-memory SQLite configuration:
```powershell
cd backend
uv run pytest -v
```

### Client Tests (57 tests)
Verifies resource sub-clients, Active Record mappings, exception code translation, and plots. All network activity is mocked offline:
```powershell
cd client
uv run pytest -v
```

---

## Highlights of What We Built

### 1. Layered REST Web Service
Built with a modular layout (Routes $\rightarrow$ Services $\rightarrow$ ORM Models) using Flask-SQLAlchemy. Holds 6 relational tables with cascade constraints: `users`, `training_plans`, `workout_days`, `exercises`, `plan_exercises`, and `session_logs`. Includes analytics aggregation services (RPE fatigue trends, volume splits, pain tracking, muscle balances) and Marshmallow schema validations.

### 2. Active Record Client SDK
Exposes sub-client managers (`client.users`, `client.plans`, `client.stats`, etc.) returning typed dataclasses. Supports the context manager protocol for connection pooling. Supports the **Active Record** pattern, allowing relationship navigation directly on objects:
```python
pb = exercise.get_personal_best(user_id)  # returns raw dictionary record
```
Includes custom HTTP-to-Python exception mappings and six distinct chart drawing triggers in the `PowerTrackPlots` mixin.

### 3. Progressive Overload Simulation
A complete simulation that compiles the wheel package and logs six weeks of training data, demonstrating progressive overload progression, custom exception mappings, cascade cascades, and Matplotlib chart generation (saving visual reports to `demo/charts/`).

---

## Authors

Developed by Group 13:
- **Mattia Loi** (mattia.loi@student.supsi.ch)
- **Antonio Falcao** (antonio.falcao@student.supsi.ch)

SUPSI — Data Science and Artificial Intelligence, Software Modelling Lab, 2025/2026
