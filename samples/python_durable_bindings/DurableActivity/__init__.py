import logging

import azure.functions as func


def main(input:str):
    logging.warn(input)
