import os
import sqlite3
from pathlib import Path

DATABASE_NAME = "results.db"

DATABASE_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / DATABASE_NAME
)


def create_connection():
    """Create and return a connection to the SQLite database."""

    connection = None

    try:
        database_path = os.getenv(
            "TEST_DATABASE_PATH",
            str(DATABASE_PATH)
        )

        connection = sqlite3.connect(database_path)

        # Enable foreign key enforcement.
        connection.execute("PRAGMA foreign_keys = ON")

        return connection

    except sqlite3.Error as error:
        print(f"Database connection error: {error}")
        return None