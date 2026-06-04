from app.services.volume import VolumeService

class IntensityService:
    @staticmethod
    def avg_rpe_by_week(plan_id):
        """
        Calculate average perceived exertion (RPE) per week for a plan.
        """
        # Fetch all logs for the plan and filter out entries without an RPE value
        logs = VolumeService.get_logs_for_plan(plan_id)
        logs = [log for log in logs if log.rpe is not None]

        week_rpe = {}
        week_count = {}

        # Aggregate RPE sum and count per week number
        for log in logs:
            week_rpe[log.week_number] = week_rpe.get(log.week_number, 0) + log.rpe
            week_count[log.week_number] = week_count.get(log.week_number, 0) + 1

        # Calculate average RPE per week
        return [
            {
                "week_number": week,
                "avg_rpe": round(week_rpe[week] / week_count[week], 2),
                "sessions_logged": week_count[week]
            }
            for week in sorted(week_rpe.keys())
        ]