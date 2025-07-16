# Test Suite for Flask Application

This directory contains comprehensive unit tests for the Flask application.

## Test Structure

- `test_main.py` - Core application tests including route testing, JSON response validation, and HTTP method testing
- `test_main_execution.py` - Tests for the main execution logic and environment variable handling
- `test_script_execution.py` - Integration tests for script execution and module structure validation
- `conftest.py` - Shared test configuration and fixtures

## Running Tests

### Run all tests:
```bash
python -m pytest tests/
```

### Run tests with verbose output:
```bash
python -m pytest tests/ -v
```

### Run tests with coverage report:
```bash
python -m pytest tests/ --cov=main --cov-report=term-missing
```

### Run tests with HTML coverage report:
```bash
python -m pytest tests/ --cov=main --cov-report=html
```

## Test Coverage

The test suite achieves 100% code coverage of the main application, testing:

- Flask application initialization
- Route functionality and responses
- JSON response structure and content
- HTTP method handling (GET, POST, PUT, DELETE)
- Error handling (404 responses)
- Environment variable configuration
- Application configuration
- Script execution capabilities

## Test Categories

### Unit Tests
- Individual function and method testing
- Flask route testing
- Configuration testing

### Integration Tests
- Full request-response cycle testing
- Multiple request handling
- Script execution testing

### Environment Tests
- Environment variable handling
- Port configuration testing
- Default value testing