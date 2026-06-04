# PowerTrack Client Library - Demo Application and Notebook

This directory contains the Demo Application and the Interactive Demonstration Notebook for the PowerTrack project. These clients demonstrate how to consume the REST API using the pre-built client library wheel (.whl).

Both the command-line script (demo.py) and the Jupyter notebook (example_usage.ipynb) showcase the full capabilities of the Python SDK, including:
- User CRUD management
- Active Record traversal (navigating from models directly)
- Cataloging and scheduling workout templates
- Performance logging (progressive overload)
- Aggregated analytics reports
- Custom HTTP error mapping to Python exceptions
- Advanced Matplotlib chart generation

---

## Prerequisites

Before executing the demo or launching the notebook, ensure you have:
1. Python 3.12+ installed on your system.
2. uv installed (a fast, modern virtual environment and package manager).
3. The Flask Backend running in a separate terminal.

---

## Setup Instructions (Step-by-Step)

Follow these steps in order to install and prepare the environment:

### Step 1: Build the Client Wheel Package
The demo application installs the client library dynamically from its built wheel package. In your terminal, navigate to the client directory and build it:

```powershell
cd client
uv build
```
This generates client-0.1.0-py3-none-any.whl inside client/dist/.

### Step 2: Start the Backend Web Service
Ensure the backend server is active and running on port 8000. In a separate terminal, navigate to the backend directory and run:

```powershell
cd backend
uv run python -m app.main
```
Verify the server is running by visiting http://127.0.0.1:8000/ in your browser.

### Step 3: Initialize the Demo Environment
Navigate to the demo directory and run uv sync to create the virtual environment and install dependencies (including Jupyter, Matplotlib, and your custom client library):

```powershell
cd demo
uv sync
```

---

## Running the Demo Clients

You can run the demo workflow using either the CLI script or the interactive notebook.

### Option A: Command-Line Interactive Script (demo.py)
This script executes the simulation inside your terminal, printing detailed debug logs for each REST call. It pauses between sections so you can inspect database changes.

To run it:
```powershell
cd demo
uv run python demo.py
```
> [!NOTE]
> Press Enter in the terminal to advance through the execution stages. On Windows, stdout is automatically wrapped in UTF-8 to prevent any encoding/unicode console crashes.

---

### Option B: Interactive Jupyter Notebook (example_usage.ipynb)
The Jupyter Notebook is the recommended option for inspecting visual charts, as it renders all Matplotlib graphs inline immediately after querying the statistics.

#### 1. Running via the Browser Interface (Jupyter Notebook Server)
Start the notebook server from the demo directory:
```powershell
uv run jupyter notebook
```
- Your web browser will automatically open to http://localhost:8888/.
- In the sidebar explorer, double-click example_usage.ipynb.
- Run the cells sequentially by pressing Shift + Enter or clicking the Run button.

#### 2. Running via VS Code / PyCharm (Recommended)
If you prefer running notebooks directly inside your IDE:
1. Open the project folder in VS Code.
2. Open the file example_usage.ipynb.
3. Click Select Kernel in the top-right corner of the editor.
4. Choose Python Environments... and select the interpreter located in the demo's virtual environment:
   - Path: demo/.venv/Scripts/python.exe (Windows) or demo/.venv/bin/python (macOS/Linux).
5. Run cells individually using the play icons.

> [!TIP]
> If you run the notebook cells multiple times, you might trigger a validation error on User Creation because the username 'marco_nb' already exists. If that happens, you can either:
> 1. Run the Section 8: Database Cleanup cell at the bottom of the notebook to clear all demo data and start fresh.
> 2. Restart the Flask backend server to clear the in-memory SQLite database, then run the notebook cells from the top.

---

## Analytics and Visual Charts Generated

Both the script and the notebook will query the client analytics modules and generate 6 distinct charts reflecting training progress, volume split, and injury status.

In the notebook, these charts are rendered directly inline. In the CLI script, they are exported as PNG files inside the demo/charts/ directory:

| Filename | Type | Description |
| :--- | :--- | :--- |
| volume_progression.png | Line (Twin-axis) | Plots single exercise volume (kg) on the left axis and average RPE on the right axis over the 6-week period. |
| total_volume.png | Bar Chart | Displays total training volume logged each week with value labels. |
| multijoint_vs_total.png | Overlapping Bar | Visualizes compound (multi-joint) exercise volume compared to total training volume. |
| rpe_trend.png | Scatter Plot | Tracks RPE over time with a horizontal dashed line highlighting high-exertion sets (RPE >= 9). |
| muscle_balance.png | Donut Chart | Shows the percentage share of training volume distributed across target muscles (Chest, Legs, etc.). |
| pain_report.png | Scatter Timeline | Highlights discomfort events by logging the week, exercise, RPE, and user feedback description. |

---


## Requirement Fulfillment Summary

This section details how the PowerTrack Demo Application fulfills the project requirements for the laboratory submission:

*   **Installs the client library from the built .whl file**
    *   The `pyproject.toml` file in this directory uses the `uv` tool to compile and install the client package dynamically from the workspace (`client = { path = "../client" }`). Additionally, the project is configured to read the pre-built `.whl` package inside `client/dist/` when building and synchronizing, ensuring complete dependency isolation.
*   **Demonstrates all CRUD operations**
    *   `demo.py` and `example_usage.ipynb` simulate a full user cycle including creating, listing, fetching, and deleting user accounts (CRUD), as well as workout plans and scheduled exercises.
*   **Demonstrates all advanced/custom operations**
    *   Tests and runs custom analytics methods (Active Record convenience bindings) on the `TrainingPlan` and `Exercise` objects such as fetching pain report history, progressive overload workload volumes, average RPEs, and personal records.
*   **Demonstrates the plot/diagram generation**
    *   Calculates and renders 6 distinct visualization charts (progression lines, workload bars, multi-joint splits, RPE scatter trends, muscle distribution donut charts, and physical pain timelines) using the `PowerTrackPlots` Matplotlib wrapper module.
*   **Can be a CLI script, interactive notebook, or simple UI - clearly documented**
    *   Offers both an interactive, step-by-step CLI script (`demo.py`) with stdout logging and a rich Jupyter Notebook (`example_usage.ipynb`) displaying inline training graphs, fully documented in this README file.
