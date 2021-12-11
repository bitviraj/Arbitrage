import datetime
import logging
from .. import arbitrage_main

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    best_case_token = arbitrage_main.get_arbitrage()
