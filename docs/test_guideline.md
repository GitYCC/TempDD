# TempDD Testing Guidelines

This document explains how to run end-to-end tests for the TempDD package.

## Test Environment Setup

### 1. Create Virtual Environment
```bash
uv venv ENV
```

### 2. Install Test Dependencies
```bash
source ENV/bin/activate && uv pip install pytest pytest-mock pytest-cov
```

### 3. Install TempDD in Development Mode
```bash
source ENV/bin/activate && uv pip install -e .
```

## Running Tests

### Run All Tests
```bash
source ENV/bin/activate && python -m pytest tests/ -v
```

### Run Specific Test File
```bash
source ENV/bin/activate && python -m pytest tests/test_commands.py -v
```

### Run Tests with Coverage Report
```bash
source ENV/bin/activate && python -m pytest tests/ -v --cov=tempdd
```
