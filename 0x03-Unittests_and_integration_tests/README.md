# Unittests and Integration Tests

This project covers the basics of writing unittests and integration tests in Python. The goal is to understand how to properly test individual functions in isolation, as well as how to test the interactions of different parts of a codebase together.

## Learning Objectives

By the end of this project, you should be able to:

- Explain the difference between unit tests and integration tests.
- Write unit tests that cover both standard cases and corner cases.
- Use mocks to isolate external dependencies such as HTTP requests, file I/O, or database access.
- Parameterize test cases to avoid repetition.
- Understand memoization and test functions decorated with it.
- Apply fixtures and common testing patterns effectively.

## Requirements

- All code is executed on Ubuntu 18.04 LTS using **Python 3.7**.
- All files must:
  - End with a new line.
  - Begin with `#!/usr/bin/env python3`.
  - Follow **pycodestyle (version 2.5)**.
  - Be executable.
- Every module, class, and function must include proper documentation strings written in full sentences.
- All functions and coroutines must use type annotations.

## Project Structure

- **utils.py**: Contains utility functions such as `access_nested_map`, `get_json`, and the `memoize` decorator.
- **client.py**: Defines the `GithubOrgClient` class which interacts with the GitHub API.
- **fixtures.py**: Contains static test data (fixtures) used in integration tests.
- **test_utils.py**: Contains unittests for `utils.py` functions.
- (Future tasks) Additional test files will be added for `client.py` and integration tests.

## How to Run Tests

You can execute tests using:

```bash
python -m unittest test_utils.py -v
