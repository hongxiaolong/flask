import pytest
import sys
import os

# Add the parent directory to the Python path so we can import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


@pytest.fixture(scope='session')
def flask_app():
    """Create and configure a new app instance for each test session."""
    app.config.update({
        "TESTING": True,
    })
    return app


@pytest.fixture
def client(flask_app):
    """A test client for the app."""
    return flask_app.test_client()


@pytest.fixture
def runner(flask_app):
    """A test runner for the app's Click commands."""
    return flask_app.test_cli_runner()