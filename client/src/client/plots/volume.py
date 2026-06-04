import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from client.plots.base import BasePlotter

class VolumePlotterMixin(BasePlotter):
    """Plotting functions related to training volume statistics."""

    def plot_volume_progression(self, plan_exercise_id: int, show: bool = True, save_path: str = None) -> None:
        """Plot week-by-week volume progression for a specific exercise."""
        data = self.client.stats.get_volume_by_exercise(plan_exercise_id)
        exercise_name = data.exercise
        weeks_data = data.data

        if not weeks_data:
            print(f"No data available for exercise {plan_exercise_id}")
            return

        weeks = [entry.week_number for entry in weeks_data]
        volumes = [entry.volume for entry in weeks_data]
        rpes = [entry.rpe for entry in weeks_data]

        fig, ax1 = plt.subplots(figsize=(10, 5))

        # Linea del volume
        ax1.plot(weeks, volumes, marker="o", color=self.COLOR_PRIMARY, linewidth=2, markersize=8, label="Volume (sets×reps×kg)")
        ax1.fill_between(weeks, volumes, alpha=0.1, color=self.COLOR_PRIMARY)
        ax1.set_xlabel("Week", fontsize=12)
        ax1.set_ylabel("Volume (kg)", fontsize=12, color=self.COLOR_PRIMARY)
        ax1.tick_params(axis="y", labelcolor=self.COLOR_PRIMARY)
        ax1.set_xticks(weeks)

        # Linea RPE sull'asse secondario
        ax2 = ax1.twinx()
        rpe_values = [r if r is not None else 0 for r in rpes]
        ax2.plot(weeks, rpe_values, marker="s", color=self.COLOR_SECONDARY, linewidth=1.5,
                 linestyle="--", markersize=6, label="RPE")
        ax2.set_ylabel("RPE (1-10)", fontsize=12, color=self.COLOR_SECONDARY)
        ax2.tick_params(axis="y", labelcolor=self.COLOR_SECONDARY)
        ax2.set_ylim(0, 11)

        # Annotazioni per settimane ad alto RPE (>= 9)
        for i, entry in enumerate(weeks_data):
            rpe = entry.rpe
            if rpe is not None and rpe >= 9:
                ax1.annotate(
                    f"RPE {rpe}",
                    xy=(weeks[i], volumes[i]),
                    xytext=(0, 15),
                    textcoords="offset points",
                    ha="center",
                    fontsize=9,
                    color=self.COLOR_WARNING,
                    arrowprops=dict(arrowstyle="->", color=self.COLOR_WARNING)
                )

        # Legenda
        blue_patch = mpatches.Patch(color=self.COLOR_PRIMARY, label="Volume (sets×reps×kg)")
        yellow_patch = mpatches.Patch(color=self.COLOR_SECONDARY, label="RPE")
        ax1.legend(handles=[blue_patch, yellow_patch], loc="upper left")

        plt.title(f"Volume & RPE Progression — {exercise_name}", fontsize=14, fontweight="bold")
        
        self._finalize_plot(show, save_path)

    def plot_total_volume(self, plan_id: int, show: bool = True, save_path: str = None) -> None:
        """Plot total weekly volume for an entire training plan."""
        data = self.client.stats.get_total_volume(plan_id)
        weeks_data = data.data

        if not weeks_data:
            print(f"No volume data available for plan {plan_id}")
            return

        weeks = [entry.week_number for entry in weeks_data]
        volumes = [entry.total_volume for entry in weeks_data]

        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(weeks, volumes, color=self.COLOR_PRIMARY, alpha=0.8, edgecolor="white", linewidth=0.5)

        # Aggiungi etichette di valore sopra ogni barra
        for bar, vol in zip(bars, volumes):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(volumes) * 0.01,
                f"{vol:,.0f}",
                ha="center", va="bottom", fontsize=9, color="#1e3a5f"
            )

        ax.set_xlabel("Week", fontsize=12)
        ax.set_ylabel("Total Volume (kg)", fontsize=12)
        ax.set_xticks(weeks)
        ax.set_title(f"Total Weekly Volume — Plan {plan_id}", fontsize=14, fontweight="bold")
        
        self._finalize_plot(show, save_path)

    def plot_multijoint_vs_total(self, plan_id: int, show: bool = True, save_path: str = None) -> None:
        """Plot multi-joint volume vs total volume per week as overlapping bars."""
        total_data = self.client.stats.get_total_volume(plan_id).data
        mj_data = self.client.stats.get_multijoint_volume(plan_id).data

        if not total_data:
            print(f"No data available for plan {plan_id}")
            return

        weeks = [entry.week_number for entry in total_data]
        total_volumes = [entry.total_volume for entry in total_data]

        mj_dict = {entry.week_number: entry.total_volume for entry in mj_data}
        mj_volumes = [mj_dict.get(w, 0) for w in weeks]

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(weeks, total_volumes, label="Total Volume", color="#93c5fd", alpha=0.9, edgecolor="white")
        ax.bar(weeks, mj_volumes, label="Multi-joint Volume", color=self.COLOR_PRIMARY, alpha=0.9, edgecolor="white")

        ax.set_xlabel("Week", fontsize=12)
        ax.set_ylabel("Volume (kg)", fontsize=12)
        ax.set_xticks(weeks)
        ax.set_title(f"Multi-joint vs Total Volume — Plan {plan_id}", fontsize=14, fontweight="bold")
        ax.legend()
        
        self._finalize_plot(show, save_path)