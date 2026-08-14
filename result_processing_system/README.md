# Result Processing System

A backend API for managing student academic results, calculating GPA/CGPA, analysing performance, ranking students, identifying at-risk students, and generating human-readable academic insights.

## 1. Project Overview

The **Result Processing System** is a Python backend application built with **FastAPI** and **SQLite**.

The system accepts student, course, and examination-result data, stores it in a relational database, processes academic scores, and exposes the results through REST API endpoints.

The project also contains:

- Academic GPA and CGPA calculations
- Student ranking and class performance statistics
- Course-level performance analysis
- Weakest and strongest course identification
- At-risk student identification
- Semester/session performance trends
- Deterministic AI-style performance insights and recommendations
- JWT authentication and role-based access control
- Centralized application and database error handling
- Automated tests with pytest

## 2. Problem

Manually processing examination results can make it difficult to:

- calculate GPA and CGPA consistently;
- rank students accurately;
- identify weak courses;
- identify students who may need academic support;
- review performance across semesters;
- expose academic results through a reusable backend API.

This project provides a structured backend solution for these tasks.

## 3. Approach

The system separates responsibilities into layers:

1. **API layer** — FastAPI routes receive requests and return HTTP responses.
2. **Schema layer** — Pydantic models validate incoming and outgoing data.
3. **Service layer** — business and database operations are separated from route handlers.
4. **Analytics layer** — Pandas-based classes calculate academic and performance statistics.
5. **Database layer** — SQLite stores users, students, courses, and results.
6. **Security layer** — bcrypt password hashing and JWT access tokens protect authenticated resources.
7. **Error-handling layer** — application exceptions are converted into structured API errors.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| FastAPI | REST API framework |
| SQLite | Relational database |
| Pandas | Academic/performance analytics |
| Pydantic | Request/response validation |
| Uvicorn | ASGI development server |
| pytest | Automated testing |
| bcrypt / Passlib | Password hashing |
| python-jose | JWT authentication |
| python-dotenv | Environment configuration |

The project requirements pin FastAPI 0.141.1, Pandas 3.0.5, pytest 9.1.1, Pydantic 2.13.4, Uvicorn 0.52.1, and related dependencies.

## 5. Project Structure

```text
.
├── app/
│   ├── analytics/
│   │   ├── advanced.py
│   │   └── performance.py
│   ├── api/
│   │   ├── dependencies.py
│   │   └── routes/
│   │       ├── academic.py
│   │       ├── admin.py
│   │       ├── advanced_analytics.py
│   │       ├── ai_insights.py
│   │       ├── analytics.py
│   │       ├── auth.py
│   │       ├── courses.py
│   │       ├── results.py
│   │       └── students.py
│   ├── core/
│   │   ├── config.py
│   │   ├── exception_handlers.py
│   │   ├── exceptions.py
│   │   └── security.py
│   ├── database/
│   │   ├── connection.py
│   │   └── tables.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── data/
│   └── results.db
├── tests/
├── .env.example
├── .gitignore
└── requirements.txt
```

## 6. Database Handling

SQLite is used as the application's relational database.

The database contains:

- `users` — authentication accounts and roles;
- `students` — student profiles;
- `courses` — course information and credit units;
- `results` — student scores linked to courses and academic sessions.

The results table stores:

- student ID;
- course ID;
- score;
- semester;
- session;
- timestamps.

The database also uses foreign keys, uniqueness constraints, validation checks, indexes, and cascading deletes.

### Sample Input

```json
{
  "student_id": 1,
  "course_code": "CSC301",
  "score": 80,
  "credit_unit": 3,
  "semester": "First",
  "session": "2025/2026"
}
```

### How data is processed

```text
Input result
     ↓
Validate score and credit unit
     ↓
Store result in SQLite
     ↓
Retrieve verified result records
     ↓
Calculate grade / grade point
     ↓
Calculate quality points
     ↓
Calculate GPA / CGPA
     ↓
Run analytics
     ↓
Return API response / insight
```

## 7. Core Logic

### Grade calculation

The service maps scores to the following grade-point scale:

| Score | Grade | Grade Point |
|---:|:---:|---:|
| 70–100 | A | 5.0 |
| 60–69 | B | 4.0 |
| 50–59 | C | 3.0 |
| 45–49 | D | 2.0 |
| 40–44 | E | 1.0 |
| 0–39 | F | 0.0 |

### Quality Point

```text
Quality Point = Grade Point × Credit Unit
```

### GPA

```text
GPA = Σ(Grade Point × Credit Unit) / Σ(Credit Units)
```

The implementation rounds the final GPA to two decimal places.

### Advanced analytics

The advanced analytics layer provides:

- grade distribution;
- average/highest/lowest score by course;
- course pass/failure rates;
- strongest courses;
- weakest courses;
- individual student performance;
- at-risk students below a configurable CGPA threshold;
- performance trend between academic periods.

### AI-style insights

The `AIInsightService` generates deterministic, human-readable explanations from verified analytics.

Importantly, the service does **not** calculate academic results itself. It consumes verified student analysis and produces explanations, reasons, and recommendations.

## 8. API Endpoints

### General

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API health/message |

### Students

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/students/` | Create student |
| GET | `/students/` | List students |
| GET | `/students/{student_id}` | Get student |
| PUT | `/students/{student_id}` | Update student |
| DELETE | `/students/{student_id}` | Delete student |

### Courses

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/courses/` | Create course |
| GET | `/courses/` | List courses |
| GET | `/courses/{course_id}` | Get course |
| PUT | `/courses/{course_id}` | Update course |
| DELETE | `/courses/{course_id}` | Delete course |

### Results

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/results/` | Create result |
| GET | `/results/` | List results |
| GET | `/results/{result_id}` | Get result |
| PUT | `/results/{result_id}` | Update result |
| DELETE | `/results/{result_id}` | Delete result |

### Academic Performance

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/academic/students/{student_id}/cgpa` | Calculate CGPA |
| GET | `/academic/students/{student_id}/gpa` | Calculate semester GPA |
| GET | `/academic/students/{student_id}/history` | View academic history |

### Analytics

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/analytics/students` | Student statistics |
| GET | `/analytics/ranking` | Student ranking |
| GET | `/analytics/class` | Class statistics |
| GET | `/analytics/courses` | Course statistics |
| GET | `/analytics/summary` | Overall performance summary |

### Advanced Analytics

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/advanced-analytics/grades` | Grade distribution |
| GET | `/advanced-analytics/courses` | Course performance |
| GET | `/advanced-analytics/courses/weakest` | Weakest courses |
| GET | `/advanced-analytics/courses/strongest` | Strongest courses |
| GET | `/advanced-analytics/students/{student_id}` | Individual analysis |
| GET | `/advanced-analytics/at-risk` | At-risk students |
| GET | `/advanced-analytics/students/{student_id}/trend` | Performance trend |

### AI Insights

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/ai-insights/students/{student_id}` | Generate performance insight |

### Authentication and Administration

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/auth/register` | Register student account/profile |
| POST | `/auth/login` | Authenticate and obtain JWT |
| GET | `/admin/dashboard` | Admin-only dashboard |

## 9. Authentication and Security

Authentication uses:

- bcrypt password hashing;
- JWT access tokens;
- configurable JWT algorithm;
- configurable token expiry;
- authenticated-user dependency;
- administrator-only dependency.

The application supports `admin`, `lecturer`, and `student` roles.

A `SECRET_KEY` is required through environment configuration.

Example `.env`:

```env
SECRET_KEY=replace-with-a-strong-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Do not commit a real secret key to GitHub.

## 10. Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd result_processing_system
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv_result_processing_system
```

Activate it in Git Bash:

```bash
source venv_result_processing_system/Scripts/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and provide a secure `SECRET_KEY`.

### 5. Run the API

```bash
uvicorn app.main:app --reload
```

### 6. Open API documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

The application creates database tables during application startup through the FastAPI lifespan handler.

## 11. Running Tests

Run the test suite with:

```bash
pytest -v
```

The supplied project dump contains **13 test modules and 106 test functions** covering areas including:

- academic calculations;
- advanced analytics;
- AI insights;
- analytics API;
- core API behavior;
- authentication;
- database behavior;
- error handling;
- performance;
- project setup;
- result-processing services.

The test configuration also creates an isolated temporary database through `TEST_DATABASE_PATH`, preventing the test suite from depending on the normal application database.

## 12. Results / Output

### Example GPA calculation

Suppose a student has:

| Course | Score | Grade Point | Credit Unit | Quality Point |
|---|---:|---:|---:|---:|
| CSC301 | 80 | 5.0 | 3 | 15 |
| MAT301 | 60 | 4.0 | 3 | 12 |
| STA301 | 55 | 3.0 | 2 | 6 |

```text
Total Quality Points = 33
Total Credit Units   = 8

GPA = 33 / 8
    = 4.13
```

### Example API response

```json
{
  "student_id": 1,
  "cgpa": 4.13
}
```

### Example performance insight

The AI-style insight endpoint can return information such as:

```json
{
  "student_id": 1,
  "student_name": "Example Student",
  "cgpa": 4.13,
  "average_score": 65.0,
  "strongest_course": "CSC301",
  "weakest_course": "STA301",
  "insight": "Example Student's current academic performance has a CGPA of 4.13...",
  "reasons": [],
  "recommendations": [
    "Maintain the current study strategy while continuing to monitor performance."
  ]
}
```

The exact response depends on the stored result data.

## 13. Screenshots

Create the following folder in the GitHub repository:

```text
screenshots/
├── api-health.png
├── swagger-students.png
├── create-result.png
├── gpa-or-cgpa.png
├── analytics-summary.png
├── ai-insight.png
└── pytest-results.png
```

Recommended screenshots for the submission:

1. API running in the terminal.
2. Swagger UI showing the available endpoints.
3. Student creation response.
4. Result creation response.
5. GPA/CGPA response.
6. Analytics response.
7. AI insight response.
8. Successful pytest output.

Update the filenames above if your actual screenshots use different names.

## 14. Presentation

The presentation supplied with this project covers:

- Problem
- Approach
- System architecture
- Data handling
- Core GPA/CGPA logic
- API endpoints
- Analytics
- Authentication/security
- Testing
- Results/output
- Conclusion

Presentation files:

- `Result_Processing_System_Presentation.pptx`
- `Result_Processing_System_Presentation.pdf`

## 15. Submission Checklist

This project is organized around the required submission areas:

- [x] Working backend API
- [x] Source code
- [x] README documentation
- [x] SQLite data handling
- [x] Core logic explanation
- [x] API/analytics output examples
- [x] Presentation slides
- [ ] Add final GitHub repository URL
- [ ] Add actual screenshots to `screenshots/`
- [ ] Confirm the final presentation PDF is linked in the GitHub README

## 16. Submission Links

Replace the repository placeholder before submitting.

- **GitHub Repository:** `<YOUR_GITHUB_REPOSITORY_URL>`
- **Presentation PDF:** `Result_Processing_System_Presentation.pdf`
- **Screenshots Folder:** `screenshots/`
- **Swagger Documentation:** `http://127.0.0.1:8000/docs` (local development)

## 17. Conclusion

The Result Processing System demonstrates a complete backend workflow for academic result management: data validation, persistence, result calculation, analytics, authentication, error handling, automated testing, and performance insights.

The project is designed so that academic calculations remain deterministic and verifiable, while the insight layer explains verified results in a human-readable form.
