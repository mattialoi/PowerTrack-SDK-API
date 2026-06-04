from client.plots.volume import VolumePlotterMixin
from client.plots.intensity import IntensityPlotterMixin
from client.plots.recovery import RecoveryPlotterMixin

class PowerTrackPlots(VolumePlotterMixin, IntensityPlotterMixin, RecoveryPlotterMixin):
    """
    Visualization interface for PowerTrack training data.
    Eredita in modo pulito tutte le funzioni grafiche suddivise per dominio.
    """
    def __init__(self, client):
        self.client = client