# azure-functions-durable-python
A Python SDK for Durable Functions.

### Development Environment Setup
1. Open your shell in this folder.
2. `python -m venv env` (or `py -m venv env`)
3. Open a vscode in this folder.
4. In vscode, hit `F1`, `Python: Select Interpreter`, select the one endswith **env**
5. In vscode shell, run `pip install -r requirements.txt`
6. In vscode, hit `F1`, `Python: Select Linter`, select **flake8**
7. Contribute by adding more code (or subtracting more code)

### Run Tests
1. Open your shell in this folder.
2. `python -m venv env` (or `py -m venv env`)
3. `env\Scripts\Activate.ps1` to activate virtual environment
4. `pip install -r requirements.txt`
5. To run test against specific test file. Use `pytest <test file>` (e.g. `.\tests\test_constants.py`)
