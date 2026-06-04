import matplotlib.pyplot as plt
from client.plots.base import BasePlotter

class RecoveryPlotterMixin(BasePlotter):
    """Plotting functions related to physical recovery and muscle balance."""

    def plot_muscle_balance(self, plan_id: int, show: bool = True, save_path: str = None) -> None:
        """Plot volume distribution by muscle group as a pie chart."""
        data = self.client.stats.get_muscle_balance(plan_id)
        muscle_data = data.data

        if not muscle_data:
            print(f"No muscle balance data available for plan {plan_id}")
            return

        labels = [entry.target_muscle for entry in muscle_data]
        sizes = [entry.total_volume for entry in muscle_data]
        colors = [self.COLOR_PRIMARY, self.COLOR_SUCCESS, self.COLOR_WARNING, "#f59e0b", "#7c3aed", "#0891b2", "#be185d"]

        fig, ax = plt.subplots(figsize=(8, 8))
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors[:len(labels)],
            autopct="%1.1f%%",
            startangle=140,
            pctdistance=0.8,
            wedgeprops=dict(edgecolor="white", linewidth=2)
        )

        for text in autotexts:
            text.set_fontsize(10)
            text.set_fontweight("bold")

        total = data.total_volume
        ax.set_title(
            f"Volume Distribution by Muscle Group — Plan {plan_id}\nTotal: {total:,.0f} kg",
            fontsize=14, fontweight="bold"
        )
        
        self._finalize_plot(show, save_path)

    def plot_pain_report(self, plan_id: int, show: bool = True, save_path: str = None) -> None:
        """Plot a timeline of pain/discomfort events for a training plan."""
        data = self.client.stats.get_pain_report(plan_id)
        pain_data = data.data
        total_flags = data.total_pain_flags

        if not pain_data:
            print(f"No pain events reported for plan {plan_id}")
            return

        weeks = [entry.week_number for entry in pain_data]
        exercises = [entry.exercise for entry in pain_data]
        rpes = [entry.rpe or 0 for entry in pain_data]

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.scatter(weeks, [1] * len(weeks), c=self.COLOR_WARNING, s=[r * 30 + 50 for r in rpes], zorder=3, alpha=0.8)

        # Annotazioni con nome dell'esercizio e RPE associato
        for week, exercise, rpe in zip(weeks, exercises, rpes):
            ax.annotate(
                f"{exercise}\n(RPE {rpe})" if rpe else exercise,
                xy=(week, 1),
                xytext=(0, 20),
                textcoords="offset points",
                ha="center",
                fontsize=9,
                color=self.COLOR_WARNING
            )

        ax.axhline(y=1, color=self.COLOR_MUTED, linewidth=1, linestyle="--", alpha=0.5)
        ax.set_xlabel("Week", fontsize=12)
        ax.set_yticks([])
        ax.set_xticks(sorted(set(weeks)))
        ax.set_title(
            f"Pain & Discomfort Report — Plan {plan_id} ({total_flags} event{'s' if total_flags != 1 else ''})",
            fontsize=14, fontweight="bold"
        )
        
        self._finalize_plot(show, save_path)