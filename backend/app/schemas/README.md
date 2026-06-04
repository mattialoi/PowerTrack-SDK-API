# Data Validation & Serialization (Marshmallow Schemas)

This package contains the **Marshmallow Schemas** used by PowerTrack to validate incoming API request bodies (Deserialization / Load) and format JSON responses (Serialization / Dump).

---

## Validation Constraints

Schemas enforce data integrity constraints at the API gateway layer:
* **Types**: Verifies that input values match required types (e.g. `sets` is an integer, `weight` is a float).
* **Positive Boundaries**: Numerical inputs such as `sets`, `reps`, `week_number`, `day_order`, `exercise_order`, and `total_weeks` must be strictly positive ($\ge 1$).
* **Loads**: `weight` must be non-negative ($\ge 0$).
* **Rating of Perceived Exertion (RPE)**: Must be an integer between 1 and 10 (inclusive) or null.
* **Enumerations**: `mechanics_type` is validated against the strict list of choices `["Multi-joint", "Isolation", "Cardio"]`.

---

## Security (Dump Only Fields)
To prevent clients from overriding database-controlled fields, parameters such as database-generated Primary Keys (`id`), creation dates (`start_date`), and analytical metrics are marked as `dump_only=True`. These fields are serialized when responding to requests, but ignored if sent in request payloads.