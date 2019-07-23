import durable_functions as df


def get_orchestrator_fn():
    output = []
    output.push(yield df.callActivity("Hello", "Tokyo"))
    output.push(yield df.callActivity("Hello", "Tokyo"))
    return output


orchestrator_fn = df.Orchestrator(get_orchestrator_fn)
