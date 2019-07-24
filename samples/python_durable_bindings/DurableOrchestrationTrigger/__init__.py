import logging

import azure.functions as func

def main(context: str):
    logging.warn(context)
