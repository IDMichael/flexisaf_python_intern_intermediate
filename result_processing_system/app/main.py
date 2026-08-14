from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.tables import create_tables
from app.core.exception_handlers import (
    app_exception_handler,
    unexpected_exception_handler,
)
from app.core.exceptions import AppException
from app.api.routes import academic
from app.api.routes import advanced_analytics
from app.api.routes import ai_insights
from app.api.routes import auth
from app.api.routes import admin
from app.api.routes import courses
from app.api.routes import results
from app.api.routes import students

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application resources."""

    create_tables()

    yield


app = FastAPI(
    title="Result Processing System",
    description=(
        "A backend service for processing "
        "student examination results."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_exception_handler(
    Exception,
    unexpected_exception_handler,
)

app.include_router(students.router)
app.include_router(courses.router)
app.include_router(results.router)
app.include_router(academic.router)
app.include_router(advanced_analytics.router)
app.include_router(ai_insights.router)
app.include_router(auth.router)
app.include_router(admin.router)

@app.get("/")
def home():
    return {
        "message": "Result Processing System API is running."
    }

