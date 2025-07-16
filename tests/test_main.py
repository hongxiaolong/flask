import pytest
import json
import os
from main import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def app_context():
    """Create an application context for testing."""
    with app.app_context():
        yield app


class TestFlaskApp:
    """Test suite for the Flask application."""

    def test_app_exists(self, app_context):
        """Test that the Flask app instance exists."""
        assert app_context is not None
        assert app_context.name == 'main'

    def test_app_is_testing(self, client):
        """Test that the app is in testing mode."""
        assert app.config['TESTING'] is True

    def test_index_route_exists(self, client):
        """Test that the index route exists and is accessible."""
        response = client.get('/')
        assert response.status_code == 200

    def test_index_route_returns_json(self, client):
        """Test that the index route returns JSON content."""
        response = client.get('/')
        assert response.content_type == 'application/json'

    def test_index_route_content(self, client):
        """Test that the index route returns the expected content."""
        response = client.get('/')
        data = json.loads(response.data)
        
        assert 'Choo Choo' in data
        assert data['Choo Choo'] == 'Welcome to Railway Flask 2024.08.01'

    def test_index_route_response_structure(self, client):
        """Test that the index route response has the correct structure."""
        response = client.get('/')
        data = json.loads(response.data)
        
        # Should be a dictionary with exactly one key
        assert isinstance(data, dict)
        assert len(data) == 1
        assert list(data.keys()) == ['Choo Choo']

    def test_nonexistent_route_returns_404(self, client):
        """Test that accessing a non-existent route returns 404."""
        response = client.get('/nonexistent')
        assert response.status_code == 404

    def test_index_route_methods(self, client):
        """Test that the index route only accepts GET requests."""
        # GET should work
        response = client.get('/')
        assert response.status_code == 200
        
        # POST should return 405 Method Not Allowed
        response = client.post('/')
        assert response.status_code == 405
        
        # PUT should return 405 Method Not Allowed
        response = client.put('/')
        assert response.status_code == 405
        
        # DELETE should return 405 Method Not Allowed
        response = client.delete('/')
        assert response.status_code == 405

    def test_response_headers(self, client):
        """Test that the response has appropriate headers."""
        response = client.get('/')
        
        # Should have Content-Type header for JSON
        assert 'Content-Type' in response.headers
        assert 'application/json' in response.headers['Content-Type']

    def test_app_configuration(self):
        """Test application configuration."""
        # Test that the app can be configured
        assert hasattr(app, 'config')
        
        # Test that we can set testing mode
        app.config['TESTING'] = True
        assert app.config['TESTING'] is True


class TestEnvironmentVariables:
    """Test suite for environment variable handling."""

    def test_port_environment_variable(self, monkeypatch):
        """Test that the PORT environment variable is handled correctly."""
        # Test default port
        assert os.getenv("PORT", default=5000) == 5000
        
        # Test custom port via environment variable
        monkeypatch.setenv("PORT", "8080")
        assert os.getenv("PORT", default=5000) == "8080"

    def test_port_default_value(self):
        """Test that the default port is 5000 when PORT env var is not set."""
        # Remove PORT env var if it exists
        if "PORT" in os.environ:
            del os.environ["PORT"]
        
        port = os.getenv("PORT", default=5000)
        assert port == 5000


class TestApplicationIntegration:
    """Integration tests for the Flask application."""

    def test_full_request_response_cycle(self, client):
        """Test a complete request-response cycle."""
        response = client.get('/')
        
        # Verify status code
        assert response.status_code == 200
        
        # Verify content type
        assert response.content_type == 'application/json'
        
        # Verify response data
        data = json.loads(response.data)
        assert data == {"Choo Choo": "Welcome to Railway Flask 2024.08.01"}
        
        # Verify response is properly formatted JSON
        assert json.dumps(data)  # Should not raise an exception

    def test_multiple_requests(self, client):
        """Test that multiple requests work consistently."""
        for _ in range(5):
            response = client.get('/')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['Choo Choo'] == 'Welcome to Railway Flask 2024.08.01'

    def test_concurrent_requests_simulation(self, client):
        """Test that the app can handle multiple requests (simulated)."""
        responses = []
        for i in range(10):
            response = client.get('/')
            responses.append(response)
        
        # All responses should be successful
        for response in responses:
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'Choo Choo' in data