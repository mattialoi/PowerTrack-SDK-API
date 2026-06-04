from unittest.mock import MagicMock, patch
import pytest
from client.plots import PowerTrackPlots
from client.client import PowerTrackClient
from client.models import (
    ExerciseVolumeReport,
    ExerciseVolumeData,
    WeeklyVolumeReport,
    WeeklyVolumeData,
    WeeklyRpeReport,
    WeeklyRpeData,
    MuscleBalanceReport,
    MuscleBalanceData,
    PainReport,
    PainLog
)

@pytest.fixture
def mock_client():
    """Fixture to create a mock PowerTrackClient."""
    client = MagicMock(spec=PowerTrackClient)
    client.stats = MagicMock()
    return client

@pytest.fixture
def plots(mock_client):
    """Fixture to initialize PowerTrackPlots with the mocked client."""
    return PowerTrackPlots(mock_client)

def test_plot_volume_progression(plots, mock_client):
    """Test plotting volume progression for a single exercise."""
    report = ExerciseVolumeReport(
        plan_exercise_id=1,
        exercise="Bench Press",
        data=[
            ExerciseVolumeData(week_number=1, sets=3, reps=5, weight=80.0, volume=1200.0, rpe=8),
            ExerciseVolumeData(week_number=2, sets=3, reps=5, weight=85.0, volume=1275.0, rpe=9)
        ]
    )
    mock_client.stats.get_volume_by_exercise.return_value = report

    with patch("matplotlib.pyplot.show") as mock_show, \
         patch("matplotlib.pyplot.savefig") as mock_savefig:
        plots.plot_volume_progression(plan_exercise_id=1, show=True, save_path="test_vol.png")
        mock_show.assert_called_once()
        mock_savefig.assert_called_once_with("test_vol.png", dpi=150, bbox_inches="tight")

def test_plot_volume_progression_empty(plots, mock_client):
    """Test plotting volume progression when no data is available."""
    report = ExerciseVolumeReport(plan_exercise_id=1, exercise="Bench Press", data=[])
    mock_client.stats.get_volume_by_exercise.return_value = report

    with patch("matplotlib.pyplot.show") as mock_show:
        plots.plot_volume_progression(plan_exercise_id=1, show=True)
        mock_show.assert_not_called()

def test_plot_total_volume(plots, mock_client):
    """Test plotting total weekly volume for a training plan."""
    report = WeeklyVolumeReport(
        plan_id=10,
        data=[
            WeeklyVolumeData(week_number=1, total_volume=5000.0),
            WeeklyVolumeData(week_number=2, total_volume=5500.0)
        ]
    )
    mock_client.stats.get_total_volume.return_value = report

    with patch("matplotlib.pyplot.show") as mock_show, \
         patch("matplotlib.pyplot.savefig") as mock_savefig:
        plots.plot_total_volume(plan_id=10, show=True, save_path="test_tot.png")
        mock_show.assert_called_once()
        mock_savefig.assert_called_once_with("test_tot.png", dpi=150, bbox_inches="tight")

def test_plot_multijoint_vs_total(plots, mock_client):
    """Test plotting multi-joint vs total weekly volume."""
    total_report = WeeklyVolumeReport(
        plan_id=10,
        data=[
            WeeklyVolumeData(week_number=1, total_volume=5000.0),
            WeeklyVolumeData(week_number=2, total_volume=5500.0)
        ]
    )
    mj_report = WeeklyVolumeReport(
        plan_id=10,
        mechanics_type="Multi-joint",
        data=[
            WeeklyVolumeData(week_number=1, total_volume=3000.0),
            WeeklyVolumeData(week_number=2, total_volume=3200.0)
        ]
    )
    mock_client.stats.get_total_volume.return_value = total_report
    mock_client.stats.get_multijoint_volume.return_value = mj_report

    with patch("matplotlib.pyplot.show") as mock_show:
        plots.plot_multijoint_vs_total(plan_id=10, show=True)
        mock_show.assert_called_once()

def test_plot_rpe_trend(plots, mock_client):
    """Test plotting weekly average RPE trend."""
    report = WeeklyRpeReport(
        plan_id=10,
        data=[
            WeeklyRpeData(week_number=1, avg_rpe=7.5, sessions_logged=3),
            WeeklyRpeData(week_number=2, avg_rpe=8.8, sessions_logged=3)
        ]
    )
    mock_client.stats.get_avg_rpe.return_value = report

    with patch("matplotlib.pyplot.show") as mock_show:
        plots.plot_rpe_trend(plan_id=10, show=True)
        mock_show.assert_called_once()

def test_plot_muscle_balance(plots, mock_client):
    """Test plotting volume distribution by muscle group."""
    report = MuscleBalanceReport(
        plan_id=10,
        total_volume=10500.0,
        data=[
            MuscleBalanceData(target_muscle="Chest", total_volume=4000.0, percentage=38.1),
            MuscleBalanceData(target_muscle="Legs", total_volume=6500.0, percentage=61.9)
        ]
    )
    mock_client.stats.get_muscle_balance.return_value = report

    with patch("matplotlib.pyplot.show") as mock_show:
        plots.plot_muscle_balance(plan_id=10, show=True)
        mock_show.assert_called_once()

def test_plot_pain_report(plots, mock_client):
    """Test plotting pain and discomfort events timeline."""
    report = PainReport(
        plan_id=10,
        total_pain_flags=1,
        data=[
            PainLog(week_number=3, exercise="Squat", rpe=8, user_feedback="Knee discomfort")
        ]
    )
    mock_client.stats.get_pain_report.return_value = report

    with patch("matplotlib.pyplot.show") as mock_show:
        plots.plot_pain_report(plan_id=10, show=True)
        mock_show.assert_called_once()