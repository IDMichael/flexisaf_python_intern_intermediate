import os
import tempfile
from pathlib import Path

import pytest

from app.database.tables import create_tables


@pytest.fixture(scope="session", autouse=True)
def test_database():
    """Create an isolated database for the test suite."""

    with tempfile.TemporaryDirectory() as temporary_directory:

        database_path = (
            Path(temporary_directory)
            / "test_results.db"
        )

        # Tell the application to use the test database.
        os.environ["TEST_DATABASE_PATH"] = str(
            database_path
        )

        # Create all application database tables.
        create_tables()

        yield database_path

        # Remove the test database setting.
        os.environ.pop(
            "TEST_DATABASE_PATH",
            None
        )