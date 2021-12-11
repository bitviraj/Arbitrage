import datetime
import logging
from .. import arbitrage_main
import pyodbc
import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    server = "LAPTOP-03Q3FH50"
    database = "arbitrage"
    cnxn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + server
        + ";DATABASE="
        + database
        + ";Trusted_Connection=yes;"
    )
    cursor = cnxn.cursor()

    result = arbitrage_main.get_arbitrage()[0]
    my_token = result["symbol"]
    my_return = (float(result["amount"]) - 1) * 100
    my_time_stamp = datetime.datetime.now()
