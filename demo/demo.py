"""
PowerTrack Client Library — Demo Application
==============================================
This script demonstrates the full capabilities of the PowerTrack client library
by simulating a realistic workout tracking workflow.

Prerequisites:
    1. Start the backend server on port 8000:
        cd backend
        uv run python -m app.main
        cd ..

    2. Run this demo:
        cd demo 
        uv run python demo.py
"""

import os
import sys
import io
import logging

# Force UTF-8 encoding for standard output on Windows to prevent UnicodeEncodeError
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from client import (
    PowerTrackClient,
    PowerTrackPlots,
    PowerTrackAPIError,
    PowerTrackNotFoundError,
    PowerTrackConflictError,
    PowerTrackValidationError
)


# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────

BASE_URL = "http://127.0.0.1:8000"
CHARTS_DIR = os.path.join(os.path.dirname(__file__), "charts")


def setup_logging():
    """Enable debug logging to see all HTTP calls made by the client."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S"
    )


def print_header(title: str):
    """Print a formatted section header."""
    width = 60
    print()
    print("=" * width)
    print(f"  {title}")
    print("=" * width)


def print_step(step: str):
    """Print a formatted sub-step."""
    print(f"\n  → {step}")


def pause():
    """Pause execution until user presses Enter."""
    input("\n  Press Enter to continue...")


# ─────────────────────────────────────────────
# DEMO SECTIONS
# ─────────────────────────────────────────────

def demo_connection(client: PowerTrackClient):
    """Section 1: Verify backend connectivity."""
    print_header("1. CONNECTION CHECK")

    if client.ping():
        print("Backend is online and reachable!")
    else:
        print("Backend is NOT reachable. Please start the server first.")
        print(f"     Expected URL: {BASE_URL}")
        sys.exit(1)

    pause()


def demo_users(client: PowerTrackClient):
    """Section 2: User management (CRUD)."""
    print_header("2. USER MANAGEMENT")

    # Create users
    print_step("Creating users...")
    user_marco = client.users.create(username="marco")
    user_sara = client.users.create(username="sara")
    print(f"  Created: {user_marco}")
    print(f"  Created: {user_sara}")

    # List all users
    print_step("Listing all users...")
    users = client.users.list()
    for u in users:
        print(f"  • {u}")

    # Get single user
    print_step(f"Fetching user with ID {user_marco.id}...")
    fetched = client.users.get(user_marco.id)
    print(f"  Fetched: {fetched}")

    # Error handling: duplicate username
    print_step("Attempting to create duplicate user 'marco'...")
    try:
        client.users.create(username="marco")
    except (PowerTrackConflictError, PowerTrackValidationError) as e:
        print(f"Expected error caught: {e}")

    # Error handling: user not found
    print_step("Attempting to fetch non-existent user (ID=9999)...")
    try:
        client.users.get(9999)
    except PowerTrackNotFoundError as e:
        print(f"Expected error caught: {e}")

    pause()
    return user_marco


def demo_plan_and_days(client: PowerTrackClient, user):
    """Section 3: Training plan and workout days."""
    print_header("3. TRAINING PLAN & WORKOUT DAYS")

    # Create plan
    print_step(f"Creating a 6-week training plan for {user.username}...")
    plan = client.plans.create(user_id=user.id, name="Hypertrophy Block A", total_weeks=6)
    print(f"  Created: {plan}")

    # Active Record: get plans from user object
    print_step("Using Active Record: user.get_plans()...")
    user_plans = user.get_plans()
    print(f"  Plans for {user.username}: {user_plans}")

    # Create workout days
    print_step("Creating workout days (Push / Pull / Legs)...")
    day_push = client.workout_days.create(plan_id=plan.id, name="Day A - Push", day_order=1)
    day_pull = client.workout_days.create(plan_id=plan.id, name="Day B - Pull", day_order=2)
    day_legs = client.workout_days.create(plan_id=plan.id, name="Day C - Legs", day_order=3)
    print(f"  Created: {day_push}")
    print(f"  Created: {day_pull}")
    print(f"  Created: {day_legs}")

    # Active Record: get days from plan object
    print_step("Using Active Record: plan.get_days()...")
    days = plan.get_days()
    for d in days:
        print(f"  • {d}")

    # Update a day
    print_step("Updating 'Day A - Push' to 'Day A - Chest & Shoulders'...")
    updated_day = client.workout_days.update(day_id=day_push.id, name="Day A - Chest & Shoulders")
    print(f"  Updated: {updated_day}")

    pause()
    return plan, day_push, day_pull, day_legs


def demo_exercises(client: PowerTrackClient):
    """Section 4: Exercise catalog management."""
    print_header("4. EXERCISE CATALOG")

    exercises_data = [
        ("Bench Press",     "Multi-joint", "Chest"),
        ("Overhead Press",  "Multi-joint", "Shoulders"),
        ("Cable Flyes",     "Isolation",   "Chest"),
        ("Barbell Row",     "Multi-joint", "Back"),
        ("Pull-Up",         "Multi-joint", "Back"),
        ("Bicep Curl",      "Isolation",   "Arms"),
        ("Squat",           "Multi-joint", "Legs"),
        ("Romanian Deadlift", "Multi-joint", "Legs"),
        ("Leg Extensions",  "Isolation",   "Legs"),
    ]

    print_step(f"Creating {len(exercises_data)} exercises in the catalog...")
    created_exercises = []
    for name, mech, muscle in exercises_data:
        ex = client.exercises.create(name=name, mechanics_type=mech, target_muscle=muscle)
        created_exercises.append(ex)
        print(f"  + {ex}")

    # Filter exercises
    print_step("Filtering exercises by target_muscle='Legs'...")
    legs = client.exercises.list(target_muscle="Legs")
    for ex in legs:
        print(f"  • {ex}")

    print_step("Filtering exercises by mechanics_type='Multi-joint'...")
    compounds = client.exercises.list(mechanics_type="Multi-joint")
    for ex in compounds:
        print(f"  • {ex}")

    pause()
    return created_exercises


def demo_scheduling(client: PowerTrackClient, day_push, day_pull, day_legs, exercises):
    """Section 5: Schedule exercises into workout days."""
    print_header("5. EXERCISE SCHEDULING")

    # Map exercises by name for convenience
    ex_map = {ex.name: ex for ex in exercises}

    # Push day exercises
    print_step("Scheduling exercises for Push day...")
    pe_bench = client.plan_exercises.create(
        workout_day_id=day_push.id, exercise_id=ex_map["Bench Press"].id,
        exercise_order=1, notes="Warm up with empty bar"
    )
    pe_ohp = client.plan_exercises.create(
        workout_day_id=day_push.id, exercise_id=ex_map["Overhead Press"].id,
        exercise_order=2
    )
    pe_flyes = client.plan_exercises.create(
        workout_day_id=day_push.id, exercise_id=ex_map["Cable Flyes"].id,
        exercise_order=3, notes="Focus on stretch at bottom"
    )
    print(f"  Scheduled: {pe_bench}")
    print(f"  Scheduled: {pe_ohp}")
    print(f"  Scheduled: {pe_flyes}")

    # Pull day exercises
    print_step("Scheduling exercises for Pull day...")
    pe_row = client.plan_exercises.create(
        workout_day_id=day_pull.id, exercise_id=ex_map["Barbell Row"].id,
        exercise_order=1
    )
    pe_pullup = client.plan_exercises.create(
        workout_day_id=day_pull.id, exercise_id=ex_map["Pull-Up"].id,
        exercise_order=2
    )
    pe_curl = client.plan_exercises.create(
        workout_day_id=day_pull.id, exercise_id=ex_map["Bicep Curl"].id,
        exercise_order=3
    )

    # Legs day exercises
    print_step("Scheduling exercises for Legs day...")
    pe_squat = client.plan_exercises.create(
        workout_day_id=day_legs.id, exercise_id=ex_map["Squat"].id,
        exercise_order=1, notes="Brace core, break at hips first"
    )
    pe_rdl = client.plan_exercises.create(
        workout_day_id=day_legs.id, exercise_id=ex_map["Romanian Deadlift"].id,
        exercise_order=2
    )
    pe_legext = client.plan_exercises.create(
        workout_day_id=day_legs.id, exercise_id=ex_map["Leg Extensions"].id,
        exercise_order=3
    )

    # Active Record: get exercises from a day
    print_step("Using Active Record: day_push.get_exercises()...")
    scheduled = day_push.get_exercises()
    for s in scheduled:
        print(f"  • {s}")

    pause()
    return {
        "bench": pe_bench, "ohp": pe_ohp, "flyes": pe_flyes,
        "row": pe_row, "pullup": pe_pullup, "curl": pe_curl,
        "squat": pe_squat, "rdl": pe_rdl, "legext": pe_legext
    }


def demo_session_logs(client: PowerTrackClient, plan_exercises: dict):
    """Section 6: Log 6 weeks of training sessions with progressive overload."""
    print_header("6. SESSION LOGGING (6 WEEKS)")

    # Realistic progressive overload data for each exercise over 6 weeks
    # Format: (sets, reps, base_weight, weight_increment_per_week, base_rpe)
    exercise_progressions = {
        "bench":  (4, 8,  60.0, 2.5, 6),
        "ohp":    (3, 10, 30.0, 1.25, 6),
        "flyes":  (3, 12, 10.0, 1.0, 5),
        "row":    (4, 8,  50.0, 2.5, 6),
        "pullup": (3, 8,  0.0,  0.0, 7),
        "curl":   (3, 12, 12.0, 1.0, 5),
        "squat":  (4, 6,  80.0, 5.0, 7),
        "rdl":    (3, 8,  60.0, 2.5, 6),
        "legext": (3, 15, 30.0, 2.0, 5),
    }

    for week in range(1, 7):
        print_step(f"Logging Week {week}...")
        for ex_key, (sets, reps, base_w, incr, base_rpe) in exercise_progressions.items():
            pe = plan_exercises[ex_key]
            weight = base_w + (incr * (week - 1))
            rpe = min(base_rpe + (week - 1), 10)  # RPE increases with fatigue

            # Simulate pain on leg extensions in week 4
            pain = (ex_key == "legext" and week == 4)
            feedback = "Slight knee discomfort during extension" if pain else None

            client.session_logs.create(
                plan_exercise_id=pe.id,
                week_number=week,
                sets=sets,
                reps=reps,
                weight=weight,
                rpe=rpe,
                user_feedback=feedback,
                pain_discomfort=pain
            )
        print(f"Week {week} logged ({len(exercise_progressions)} exercises)")

    # Active Record: get logs from a plan exercise
    print_step("Using Active Record: pe_bench.get_logs()...")
    bench_logs = plan_exercises["bench"].get_logs()
    for log in bench_logs:
        print(f"  Week {log.week_number}: {log.sets}x{log.reps} @ {log.weight}kg (RPE {log.rpe})")

    pause()


def demo_statistics(client: PowerTrackClient, plan, user, exercises, plan_exercises: dict):
    """Section 7: Retrieve and display training statistics."""
    print_header("7. TRAINING STATISTICS")

    # Total volume
    print_step("Total weekly volume for the plan...")
    vol = client.stats.get_total_volume(plan.id)
    for entry in vol.data:
        print(f"  Week {entry.week_number}: {entry.total_volume:,.0f} kg")

    # Multi-joint volume
    print_step("Multi-joint weekly volume...")
    mj_vol = client.stats.get_multijoint_volume(plan.id)
    for entry in mj_vol.data:
        print(f"  Week {entry.week_number}: {entry.total_volume:,.0f} kg")

    # Average RPE
    print_step("Average RPE per week...")
    rpe = client.stats.get_avg_rpe(plan.id)
    for entry in rpe.data:
        print(f"  Week {entry.week_number}: avg RPE = {entry.avg_rpe:.1f} ({entry.sessions_logged} sessions)")

    # Muscle balance
    print_step("Volume distribution by muscle group...")
    balance = client.stats.get_muscle_balance(plan.id)
    print(f"  Total Volume: {balance.total_volume:,.0f} kg")
    for entry in balance.data:
        bar = "█" * int(entry.percentage / 2)
        print(f"  {entry.target_muscle:12s} {bar} {entry.percentage:.1f}%")

    # Pain report
    print_step("Pain and discomfort report...")
    pain = client.stats.get_pain_report(plan.id)
    print(f"  Total pain flags: {pain.total_pain_flags}")
    for entry in pain.data:
        print(f"Week {entry.week_number}: {entry.exercise} (RPE {entry.rpe}) — {entry.user_feedback}")

    # Personal best
    ex_map = {ex.name: ex for ex in exercises}
    print_step("Personal best for Squat...")
    pb_squat = client.stats.get_personal_best(user.id, ex_map["Squat"].id)
    print(f"  Max weight: {pb_squat['max_weight']} kg × {pb_squat['reps_at_max']} reps (Week {pb_squat['week_achieved']})")

    # Active Record: personal best from exercise object
    print_step("Using Active Record: exercise.get_personal_best(user_id)...")
    pb_bench = ex_map["Bench Press"].get_personal_best(user.id)
    print(f"  Bench Press PR: {pb_bench['max_weight']} kg × {pb_bench['reps_at_max']} reps (Week {pb_bench['week_achieved']})")

    pause()


def demo_charts(client: PowerTrackClient, plan, plan_exercises: dict):
    """Section 8: Generate and save training charts as PNG files."""
    print_header("8. CHART GENERATION")

    os.makedirs(CHARTS_DIR, exist_ok=True)
    plots = PowerTrackPlots(client)

    charts = [
        ("Volume Progression (Bench Press)",
         lambda: plots.plot_volume_progression(plan_exercises["bench"].id, show=False,
                                                save_path=os.path.join(CHARTS_DIR, "volume_progression.png"))),
        ("Total Weekly Volume",
         lambda: plots.plot_total_volume(plan.id, show=False,
                                         save_path=os.path.join(CHARTS_DIR, "total_volume.png"))),
        ("Multi-joint vs Total Volume",
         lambda: plots.plot_multijoint_vs_total(plan.id, show=False,
                                                 save_path=os.path.join(CHARTS_DIR, "multijoint_vs_total.png"))),
        ("RPE Trend",
         lambda: plots.plot_rpe_trend(plan.id, show=False,
                                      save_path=os.path.join(CHARTS_DIR, "rpe_trend.png"))),
        ("Muscle Balance",
         lambda: plots.plot_muscle_balance(plan.id, show=False,
                                           save_path=os.path.join(CHARTS_DIR, "muscle_balance.png"))),
        ("Pain Report",
         lambda: plots.plot_pain_report(plan.id, show=False,
                                         save_path=os.path.join(CHARTS_DIR, "pain_report.png"))),
    ]

    for name, generate in charts:
        print_step(f"Generating: {name}...")
        generate()
        print(f"    Saved")

    print(f"\nAll charts saved to: {CHARTS_DIR}")
    pause()


def demo_cleanup(client: PowerTrackClient, user):
    """Section 9: Clean up demo data."""
    print_header("9. CLEANUP")

    print_step(f"Deleting user '{user.username}' and all associated data (cascade)...")
    result = client.users.delete(user.id)
    print(f"  {result}")

    # Delete sara too
    users = client.users.list()
    for u in users:
        if u.username == "sara":
            client.users.delete(u.id)
            print(f"  Deleted user 'sara'")

    # Clean up exercises
    print_step("Deleting all catalog exercises...")
    for ex in client.exercises.list():
        client.exercises.delete(ex.id)
        print(f"  Deleted: {ex.name}")

    print("\nAll demo data cleaned up successfully!")


# ─────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────

def main():
    """Run the complete PowerTrack client library demo."""
    print()
    print("+" + "="*60 + "+")
    print("|         PowerTrack Client Library - Full Demo              |")
    print("|                                                            |")
    print("|  This demo showcases all features of the client library:   |")
    print("|  - CRUD operations on all resources                        |")
    print("|  - Active Record pattern (Rich Domain Model)               |")
    print("|  - Custom exception handling                               |")
    print("|  - Training statistics and analytics                       |")
    print("|  - Chart generation with Matplotlib                        |")
    print("|  - Context Manager support                                 |")
    print("+" + "="*60 + "+")

    pause()

    # Uncomment the following line to see all HTTP debug logs:
    # setup_logging()

    # Use Context Manager to ensure session cleanup
    with PowerTrackClient(BASE_URL) as client:

        # 1. Connection check
        demo_connection(client)

        # 2. User management
        user = demo_users(client)

        # 3. Plan and workout days
        plan, day_push, day_pull, day_legs = demo_plan_and_days(client, user)

        # 4. Exercise catalog
        exercises = demo_exercises(client)

        # 5. Schedule exercises into days
        plan_exercises = demo_scheduling(client, day_push, day_pull, day_legs, exercises)

        # 6. Log 6 weeks of training
        demo_session_logs(client, plan_exercises)

        # 7. View statistics
        demo_statistics(client, plan, user, exercises, plan_exercises)

        # 8. Generate charts
        demo_charts(client, plan, plan_exercises)

        # 9. Clean up
        demo_cleanup(client, user)

    # Session closed automatically by Context Manager

    print()
    print("+" + "="*60 + "+")
    print("|              Demo completed successfully!                  |")
    print("+" + "="*60 + "+")
    print()


if __name__ == "__main__":
    main()