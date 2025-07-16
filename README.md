---
title: Flask
description: A popular minimal server framework for Python
tags:
  - python
  - flask
---

# Python Flask Example

This is a [Flask](https://flask.palletsprojects.com/en/1.1.x/) app that serves a simple JSON response.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/zUcpux)

## ✨ Features

- Python
- Flask

## 💁‍♀️ How to use

- Install Python requirements `pip install -r requirements.txt`
- Start the server for development `python3 main.py`

## 🧪 Testing

This project includes a comprehensive test suite with 100% code coverage.

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run tests with coverage report
python -m pytest tests/ --cov=main --cov-report=term-missing

# Run tests using the test runner script
python run_tests.py
```

### Test Coverage

- **Total Tests**: 24
- **Code Coverage**: 100%
- **Test Categories**: Unit tests, Integration tests, Environment tests

The test suite covers:
- Flask application functionality
- Route testing and HTTP methods
- JSON response validation
- Environment variable handling
- Error handling (404 responses)
- Application configuration
- Script execution capabilities
