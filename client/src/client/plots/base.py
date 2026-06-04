import matplotlib.pyplot as plt

class BasePlotter:
    """Base class for plotters offering common utilities like saving and showing charts."""

    # color palette for consistent styling across all plots
    COLOR_PRIMARY = "#2563eb"    # Blue
    COLOR_SECONDARY = "#f59e0b"  # Amber (RPE)
    COLOR_WARNING = "#dc2626"    # Red (warning/pain)
    COLOR_SUCCESS = "#16a34a"    # Green
    COLOR_MUTED = "#94a3b8"      # Grey Slate

    def _finalize_plot(self, show: bool = True, save_path: str = None) -> None:
        """Helper to apply tight layout, save to disk if path is provided, show, and close figure."""
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches="tight")
        if show:
            plt.show()
        plt.close()