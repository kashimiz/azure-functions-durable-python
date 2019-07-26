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


### Debug E2E with azure-functions-durable-extension
1. Open a new Powershell section
2. Change directory to `samples\durable_cli`
3. Drop the restriction policy in Powershell process `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Unrestricted`
4. Run `.\setup.ps1`. You should have the latest durable function supports in `func` command
5. Change directory to `samples\python_durable_bindings`
6. Run `func extensions install`
7. Copy and replace all files from `samples\python_durable_bindings\BinReplace` to `samples\python_durable_bindings\bin`
8. Create a python virtual environment `py -m venv env` or `python -m venv env` (preferred python 3.6)
9. Activate virtual environment `env\Scripts\Activate.ps1`
10. Install python dependencies `pip install -r requirements.txt`
11. Create a new file `local.settings.json` in `samples\python_durable_bindings` with the following content

```
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "<Storage Connection String>",
    "FUNCTIONS_WORKER_RUNTIME": "python"
  }
}
```

12. Run `func host start`
13. Invoke the Sequence Orchestrator by `POST http://localhost:7071/runtime/webhooks/durabletask/orchestrators/DurableOrchestrationTrigger`
14. Invoke the Fanout Orchestrator by `POST http://localhost:7071/runtime/webhooks/durabletask/orchestrators/DurableFanoutOrchestrationTrigger`


### Run Tests
1. Open your shell in this folder.
2. `python -m venv env` (or `py -m venv env`)
3. `env\Scripts\Activate.ps1` to activate virtual environment
4. `pip install -r requirements.txt`
5. To run test against specific test file. Use `pytest <test file>` (e.g. `.\tests\test_constants.py`)


### Run E2E in development mode
1. Get a sample functionapp (e.g. [sample function](https://github.com/Hazhzeng/python-durable-function))
2. Get the latest `npm install -g azure-functions-core-tools`
3. Open your shell, cd into your **sample function**
4. `python -m venv env` (or `py -m venv env`)
5. `env\Scripts\Activate.ps1` to activate virtual environment
6. `pip install -r requirements.txt`
7. Install durable python library with `pip install -e <azure-functions-durable-python location>`
8. Install durable host extension with `func extensions install -p Microsoft.Azure.WebJobs.Extensions.DurableTask -v 1.8.3`
9. Run your **sample function** with `func host start`
10. Trigger orchistrator with `Invoke-WebRequest -Method Post http://localhost:<port>/api/<orchestrators route>` (e.g. `Invoke-WebRequest -Method Post -Uri http://localhost:7071/api/orchestrators/DurableFunctionsOrchestratorPY`)
