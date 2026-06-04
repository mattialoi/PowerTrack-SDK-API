# REST API Blueprints & Routing

This package contains the Flask Blueprints handling incoming HTTP requests, route mapping, and API endpoints.

---

## API Route Endpoint Reference

| Endpoint | HTTP Method | Service / Action | Description |
| :--- | :--- | :--- | :--- |
| `/users/` | `GET` | `UserService.get_all` | List all users |
| `/users/` | `POST` | `UserService.create` | Register a new user |
| `/users/<id>` | `GET` / `DELETE` | `UserService` | Retrieve or delete a user |
| `/plans/` | `GET` / `POST` | `PlanService` | List or create training plans |
| `/plans/<id>` | `GET` / `PUT` / `DELETE` | `PlanService` | Retrieve, edit, or delete a plan |
| `/plans/user/<user_id>` | `GET` | `PlanService.get_by_user` | List all plans for a specific user |
| `/workout-days/` | `POST` | `WorkoutDayService.create` | Create a workout day |
| `/workout-days/<id>` | `GET` / `PUT` / `DELETE` | `WorkoutDayService` | Retrieve, update, or delete a day |
| `/workout-days/plan/<plan_id>` | `GET` | `WorkoutDayService.get_by_plan` | List workout days for a plan |
| `/exercises/` | `GET` / `POST` | `ExerciseService` | List catalog exercises or add new ones |
| `/exercises/<id>` | `GET` / `DELETE` | `ExerciseService` | Retrieve or delete a catalog exercise |
| `/plan-exercises/` | `POST` | `PlanExerciseService.create`| Schedule an exercise into a workout day |
| `/plan-exercises/<id>` | `GET` / `PUT` / `DELETE` | `PlanExerciseService` | Retrieve, update, or delete scheduling |
| `/plan-exercises/day/<day_id>`| `GET` | `PlanExerciseService.get_by_day` | List scheduled exercises for a day |
| `/session-logs/` | `POST` | `SessionLogService.create` | Log a training session week metrics |
| `/session-logs/<id>`| `GET` / `PUT` / `DELETE` | `SessionLogService` | Retrieve, edit, or delete a logged set |
| `/session-logs/plan-exercise/<pe_id>` | `GET` | `SessionLogService` | List week logs for a scheduled exercise |
| `/stats/volume/exercise/<pe_id>` | `GET` | `VolumeService` | Weekly volume progression chart data |
| `/stats/volume/total/<plan_id>` | `GET` | `VolumeService` | Total weekly volume for a plan |
| `/stats/volume/multi-joint/<plan_id>` | `GET` | `VolumeService` | Weekly volume of compound lifts |
| `/stats/rpe/<plan_id>` | `GET` | `IntensityService` | Weekly average perceived exertion (RPE) |
| `/stats/pain/<plan_id>` | `GET` | `RecoveryService` | Report on logged pain/discomfort events |
| `/stats/muscle-balance/<plan_id>` | `GET` | `VolumeService` | Muscle group training volume breakdown |
| `/stats/personal-bests/<user_id>/<ex_id>` | `GET` | `PersonalBestsService` | Get personal record weight for an exercise |

---

## Error Handling
Validation failures and business logic exceptions are formatted as JSON responses with HTTP status codes:
- **`400 Bad Request`**: Raised on validation errors (e.g. invalid RPE values or missing fields) and returns a structured dictionary of failures.
- **`404 Not Found`**: Raised when resources or parent foreign keys do not exist in the database.
- **`409 Conflict`**: (Legacy, now mapped to 400 validation error) returned when trying to create a resource with a duplicate unique constraint (e.g., unique exercise name).


### Tests with POSTMAN note
``` 
In Key write:   Content-Type
In Value write: application/json
```