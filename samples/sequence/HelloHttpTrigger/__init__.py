# To be discussed
import logging
import durable_functions as df
import azure.functions as func
from durable_functions.models import binding_context


async def main(req: func.HttpRequest, context: binding_context) -> func.HttpResponse:
    client = df.get_client(context)
    instance_id = await client.start_new(req.params.functionName, "HelloSequence", req.body)
    logging.info(f'Started orchestration with ID = {instance_id}')
    return client.create_check_status_response(context.binding_data.req, instance_id)
