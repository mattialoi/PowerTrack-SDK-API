# Lab Project — Requirements Checklist

> **Deadline:** Sunday, 31 May 2026 at 23:59  
> **Team:** Mattia Loi, Antonio Falcao

---

## 1. Backend Web Service

Built with **Flask** or **FastAPI**.

### Database
- [ ] Connect to a database (SQLite, PostgreSQL, MySQL, or similar)
- [ ] Define at least one data model/table appropriate for the chosen domain

### Core CRUD Endpoints
- [ ] `GET` — retrieve a single resource by ID or filter
- [ ] `GET` — retrieve a list of resources
- [ ] `POST` — create a new resource
- [ ] `PUT` / `PATCH` — update an existing resource
- [ ] `DELETE` — remove a resource

### Advanced Operations
- [ ] At least one aggregation or statistics endpoint (e.g. averages, counts, rankings)
- [ ] At least one custom/domain-specific query (e.g. filtering by date range, top-N results)

### Code Quality
- [ ] Object-oriented design — logic encapsulated in classes and modules
- [ ] Correct application of course concepts (separation of concerns, reusability, etc.)
- [ ] Virtual environment managed with `uv`, `pipenv`, or `conda`
- [ ] Full unit test coverage (`pytest` recommended)

---

## 2. Client Library

A Python package that allows developers to interact with the web service programmatically.

### API Wrapper
- [ ] One method per exposed backend operation (mirrors all CRUD and advanced endpoints)
- [ ] Clean, intuitive interface — hides HTTP details from the caller
- [ ] Proper error handling (HTTP errors, connection issues, unexpected responses)

### Data Visualisation
- [ ] At least one plot or diagram generated from data returned by the web service
- [ ] Use a plotting library such as `matplotlib`, `plotly`, or `seaborn`

### Code Quality
- [ ] Object-oriented design — class-based structure
- [ ] Virtual environment managed with `uv`, `pipenv`, or `conda`
- [ ] Full unit test coverage — use mocks for HTTP calls
- [ ] Built and distributed as a **wheel package** (`.whl`)
  - [ ] `pyproject.toml` (or `setup.py`) correctly configured
  - [ ] Package installable via `pip install <name>.whl`

---

## 3. Demo Application

A standalone application that depends on the client library and showcases all implemented features.

- [ ] Installs the client library from the built `.whl` file
- [ ] Demonstrates all CRUD operations
- [ ] Demonstrates all advanced/custom operations
- [ ] Demonstrates the plot/diagram generation
- [ ] Can be a CLI script, interactive notebook, or simple UI — clearly documented

---

## 4. General & Infrastructure

### Git Repository (SUPSI GitLab)
- [ ] All source code versioned in the provided repository
- [ ] Code pushed to the `main` branch before the deadline
- [ ] Meaningful, frequent commits throughout development

### README
- [ ] Project description and chosen domain
- [ ] Instructions to set up the virtual environment
- [ ] Instructions to install dependencies
- [ ] Instructions to run the backend service
- [ ] Instructions to install the client library (from `.whl`)
- [ ] Instructions to run the demo application
- [ ] Any other information useful to a developer or evaluator

### Final Presentation
- [ ] Presented during the last week of the semester
- [ ] Covers implemented features and design decisions
- [ ] Q&A session with the course instructors


## Grading Criteria (summary)

| Area | What is evaluated |
|---|---|
| Features | Correct implementation per requirements and constraints |
| Code quality | OOP, best practices, course concepts applied correctly |
| README | Completeness, clarity, setup instructions |
| Presentation | Content, form, and delivery |
| Q&A | Understanding and ability to discuss design choices |