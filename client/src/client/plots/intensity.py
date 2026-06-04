import matplotlib.pyplot as plt
from client.plots.base import BasePlotter

class IntensityPlotterMixin(BasePlotter):
    """Plotting functions related to training effort/intensity."""

    def plot_rpe_trend(self, plan_id: int, show: bool = True, save_path: str = None) -> None:
        """Plot average RPE per week for a training plan."""
        data = self.client.stats.get_avg_rpe(plan_id)
        weeks_data = data.data

        if not weeks_data:
            print(f"No RPE data available for plan {plan_id}")
            return

        weeks = [entry.week_number for entry in weeks_data]
        rpes = [entry.avg_rpe for entry in weeks_data]
        colors = [self.COLOR_WARNING if r > 8.5 else self.COLOR_PRIMARY for r in rpes]

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(weeks, rpes, color=self.COLOR_MUTED, linewidth=1.5, linestyle="--", zorder=1)
        ax.scatter(weeks, rpes, c=colors, s=100, zorder=2)

        # Linea di soglia per sforzo elevato
        ax.axhline(y=8.5, color=self.COLOR_WARNING, linestyle=":", linewidth=1, alpha=0.6, label="High effort threshold (8.5)")

        # Annotazioni per ogni punto
        for week, rpe, color in zip(weeks, rpes, colors):
            ax.annotate(
                f"{rpe}",
                xy=(week, rpe),
                xytext=(0, 10),
                textcoords="offset points",
                ha="center",
                fontsize=9,
                color=color
            )

        ax.set_xlabel("Week", fontsize=12)
        ax.set_ylabel("Average RPE", fontsize=12)
        ax.set_xticks(weeks)
        ax.set_ylim(0, 11)
        ax.set_title(f"Average RPE per Week — Plan {plan_id}", fontsize=14, fontweight="bold")
        ax.legend()
        
        self._finalize_plot(show, save_path)