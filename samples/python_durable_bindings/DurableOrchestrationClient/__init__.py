import logging
import azure.functions as func

def main(req: func.HttpRequest, starter: str) -> str:
    logging.warn(f"req.params = {req.params}")
    logging.warn(f"starter = {starter}")
    return func.HttpResponse(status_code=200, body="success")
