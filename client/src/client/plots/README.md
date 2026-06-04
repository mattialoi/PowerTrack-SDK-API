# `plots/` — Data Visualization Module

This package provides visual chart generators for training metrics. It uses **Matplotlib** to query the sub-client REST stats service in the background and plot graphs of training volume progress, intensity fatigue, muscle balance distribution, and discomfort logs.

---

## Mixin-based Architecture

The visualization interface is built using Python **multiple inheritance (mixins)** to separate chart definitions by domain, while exposing all functions on a single root class `PowerTrackPlots`:

```
                 ┌───────────────────────┐
                 │       BasePlotter     │  (base.py)
                 │  - Color tokens       │
                 │  - finalize logic     │
                 └───────────┬───────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ VolumePlotter   │ │ IntensityPlotter│ │ RecoveryPlotter │ (Mixins)
│     Mixin       │ │     Mixin       │ │     Mixin       │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │    PowerTrackPlots    │  (__init__.py)
                 │   Main root plotter   │
                 └───────────────────────┘
```

The main class is initialized with a `PowerTrackClient` instance:
```python
from client import PowerTrackClient, PowerTrackPlots

with PowerTrackClient("http://127.0.0.1:8000") as client:
    plots = PowerTrackPlots(client)
    # Trigger plotting methods directly on the instance:
    plots.plot_total_volume(plan_id=1)
```

---

## Styling Configuration

All plotters inherit from `BasePlotter` which establishes visual styling tokens to ensure clean, consistent aesthetics across all rendered PNG charts:

- **`COLOR_PRIMARY`** (`#2563eb` - Sleek Blue): Represents workload tonnage and primary metrics.
- **`COLOR_SECONDARY`** (`#f59e0b` - Amber/Orange): Highlights secondary trends (such as RPE indices).
- **`COLOR_WARNING`** (`#dc2626` - Vibrant Red): Flags high exertion metrics (RPE $\ge 9$) and physical pain.
- **`COLOR_SUCCESS`** (`#16a34a` - Forest Green): Highlights recovery/balance achievements.
- **`COLOR_MUTED`** (`#94a3b8` - Slate Gray): Used for grid lines, connectors, and secondary lines.

Every chart method automatically delegates cleanup and saving to `_finalize_plot(show, save_path)` to ensure figures are closed and memory is freed:
- `plt.tight_layout()` is applied to prevent text overlaps.
- Saves the figure if `save_path` is provided (with a high-definition 150 DPI setting).
- Displays the chart window if `show=True`.
- Calls `plt.close()` to release Matplotlib resources.

---

## Chart Categories

### 1. Volume Progression Mixin (`volume.py`)
Tracks workload volumes ($sets \times reps \times weight$) to verify progressive overload.

* **`plot_volume_progression(plan_exercise_id: int, show: bool = True, save_path: str = None)`**
  * Plots a week-by-week line chart showing the total tonnage lifted for a specific scheduled exercise.
  * Overlays a secondary Y-axis dashed line representing logged RPE levels.
  * Draws warning callouts pointing out sets executed at extreme exertion (RPE $\ge 9$).
* **`plot_total_volume(plan_id: int, show: bool = True, save_path: str = None)`**
  * Plots a vertical bar chart showing total tonnage lifted across all exercises in a plan for each week.
  * Annotates the exact tonnage value above each bar.
* **`plot_multijoint_vs_total(plan_id: int, show: bool = True, save_path: str = None)`**
  * Plots overlapping bar charts comparing total weekly tonnage against compound, multi-joint exercise tonnage. Helps verify the proportion of compound lifts in a program.

### 2. Effort & Intensity Mixin (`intensity.py`)
Tracks RPE ratings to verify workout fatigue and target intensities.

* **`plot_rpe_trend(plan_id: int, show: bool = True, save_path: str = None)`**
  * Plots a weekly scatter and line plot mapping the athlete's average Rate of Perceived Exertion.
  * Draws a horizontal dotted line at RPE $8.5$ to demarcate high exertion thresholds. Points above this line are highlighted in red.

### 3. Recovery & Muscle splits Mixin (`recovery.py`)
Tracks muscle group balance and pain flags to monitor physical recovery.

* **`plot_muscle_balance(plan_id: int, show: bool = True, save_path: str = None)`**
  * Renders a pie chart breaking down the percentage distribution of total training volume across targeted muscles (e.g. Legs, Chest, Back, Arms).
* **`plot_pain_report(plan_id: int, show: bool = True, save_path: str = None)`**
  * Renders a timeline logging physical discomfort flags.
  * Draws warning points sized proportionally to the RPE logged during the incident, annotated with the exercise name and user feedback details.
