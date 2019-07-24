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
1. Get a sample functionapp (e.g. [sample function](https://github.com/Hazhzeng/python-durable-function))
2. Get the latest `npm install -g azure-functions-core-tools`
3. Open your shell, cd into your **sample function**
4. `python -m venv env` (or `py -m venv env`)
5. `env\Scripts\Activate.ps1` to activate virtual environment
6. `pip install -r requirements.txt`
7. `pip install ptvsd==4.2.10`
7. Install durable python library with `pip install -e <azure-functions-durable-python location>`
8. Install durable host extension with `func extensions install -p Microsoft.Azure.WebJobs.Extensions.DurableTask -v 1.8.3`
9. Clone the latest [azure-functions-durable-extension](https://github.com/Azure/azure-functions-durable-extension)
10. Build the azure-functions-durable-extension project in visual studio.
11. Replace the extension by copying the binary file to your `<sample functionapp>/bin`.
12. Replace the `<sample functionapp>/.vscode/launch.json` with the following content

```javascript
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Attach to Python Functions",
            "type": "python",
            "request": "attach",
            "port": 9091,
            "preLaunchTask": "func: host start"
        }
    ]
}
```
13. Replace the `<sample functionapp>/host.json` with the following content

```javascript
{
    "version":  "2.0",
    "extensions": {
        "durableTask": {
            "hubName": "MyTaskHub8"
        }
    }
}
```

13. Add breakpoints in **sample functionapp**. Press **F5** to launch the vscode debugger in **sample functionapp**
14. Open azure-functions-durable-extension Visual Studio solution, debug -> attach to process **func.exe**
15. Initiate a post request `Invoke-WebRequest -Method Post -Uri http://localhost:7071/runtime/webhooks/durabletask/orchestrators/DurableFunctionsOrchestratorPY?code=yYfKWggVUA3SaVL5FSodVQ1o4eOX8RAtmmJq7MwlaHwRcrDq2Y7WFQ==`
16. You should be able to see the logs in **sample functionapp** vscode's console.

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
