from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_application_starts():
    """Verify that the FastAPI application starts successfully."""

    response = client.get("/")

    assert response.status_code == 200


def test_root_endpoint_returns_expected_message():
    """Verify the root endpoint response."""

    response = client.get("/")

    assert response.json() == {
        "message": "Result Processing System API is running."
    }


def test_project_data_directory_exists():
    """Verify that the data directory exists."""

    project_root = Path(__file__).resolve().parents[1]

    data_directory = project_root / "data"

    assert data_directory.exists()
    assert data_directory.is_dir()


def test_app_package_exists():
    """Verify that the application package exists."""

    project_root = Path(__file__).resolve().parents[1]

    app_directory = project_root / "app"

    assert app_directory.exists()
    assert app_directory.is_dir()


def test_main_module_exists():
    """Verify that the FastAPI main module exists."""

    project_root = Path(__file__).resolve().parents[1]

    main_file = project_root / "app" / "main.py"

    assert main_file.exists()
    assert main_file.is_file()