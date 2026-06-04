import os
from flask import Flask, jsonify
from .database import db

def create_app(config_override=None):
    """
    Application factory function to configure and initialize the Flask application.
    """
    app = Flask(__name__)
    
    # Path management for the database
    # This path points to the 'data' folder in the root directory of the project
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    db_path = os.path.join(BASE_DIR, "data", "fitness.db")
    
    # SQLAlchemy configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Test configuration override (for testing purposes)
    if config_override:
        app.config.update(config_override)
    
    # Initialize the database with the application instance
    db.init_app(app)
    
    # ----------------------------------------------------------------
    # Blueprint Registration
    # ----------------------------------------------------------------
    from .routes.users import users_bp
    from .routes.plans import plans_bp
    from .routes.workout_days import workout_days_bp
    from .routes.exercises import exercises_bp
    from .routes.plan_exercises import plan_exercises_bp
    from .routes.session_logs import session_logs_bp
    
    from .routes.stats import stats_bp

    
    app.register_blueprint(users_bp)
    app.register_blueprint(plans_bp)
    app.register_blueprint(workout_days_bp)
    app.register_blueprint(exercises_bp)
    app.register_blueprint(plan_exercises_bp)
    app.register_blueprint(session_logs_bp)
    
    app.register_blueprint(stats_bp)
    
    # ----------------------------------------------------------------
    # Automatic Database Tables Creation
    # ----------------------------------------------------------------
    with app.app_context():
        # Models are imported here to ensure SQLAlchemy is aware of them
        # before running the table creation process
        from .models.user import User
        from .models.exercise import Exercise
        from .models.training_plan import TrainingPlan
        from .models.workout_day import WorkoutDay
        from .models.plan_exercise import PlanExercise
        from .models.session_log import SessionLog
        
        db.create_all()
    
    from werkzeug.exceptions import HTTPException

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({"error": e.description or e.name}), e.code

    # Base route for API health check
    @app.route('/')
    def index():
        return {"message": "PowerTrack API online", "status": 200}
        
    return app


if __name__ == '__main__':
    app = create_app()
    # Explicitly setting host and port 8000 for Windows/Mac compatibility
    app.run(host="127.0.0.1", port=8000, debug=True)