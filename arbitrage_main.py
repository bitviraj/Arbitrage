import requests
import os
import arbitrage_tokens
from dotenv import load_dotenv
import asyncio
import aiohttp
from datetime import datetime
import time
from web3 import Web3


load_dotenv()

bsc = os.getenv("BSC")
w3 = Web3(Web3.HTTPProvider(bsc))

start = datetime.now()

tokens = arbitrage_tokens.token_address

base_token = os.getenv("base_token")

start_amount = 3 * 10 ** 17

wallet = os.getenv("wallet")

url_swap = os.getenv("url_swap")

url_quote = os.getenv("url_quote")

balance_start = w3.eth.get_balance(wallet)
print("Balance at the start is {}".format(balance_start))


def get_tasks(session):
    tasks = []
    for token in tokens:
        tasks.append(
            session.get(
                url_swap.format(
                    base_token,
                    token,
                    start_amount,
                    wallet,
                )
            )
        )
    return tasks


async def get_quote():
    results = []

    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            if response.status == 200:
                results.append(await response.json())
    return results


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
quotes1 = asyncio.run(get_quote())


time.sleep(63)


def get_tasks2(session):
    tasks = []
    for quote1 in quotes1:
        tasks.append(
            session.get(
                url_quote.format(
                    quote1["toToken"]["address"],
                    base_token,
                    quote1["toTokenAmount"],
                )
            )
        )
    return tasks


async def get_quote2():
    results = []
    async with aiohttp.ClientSession() as session2:
        tasks = get_tasks2(session2)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            if response.status == 200:
                results.append(await response.json())

    return results


quotes2 = asyncio.run(get_quote2())

arbs = []
for quote2 in quotes2:
    arbs.append(
        {
            "symbol": quote2["fromToken"]["symbol"],
            "amount": float(quote2["toTokenAmount"]) / start_amount,
        }
    )

# print(arbs)

ready_for_swap = []
for arb in arbs:
    if float(arb["amount"]) > 1:
        ready_for_swap.append(arb)

# print(ready_for_swap)

best_swap = [{"symbol": "", "amount": 0}]
for ready in ready_for_swap:
    if int(ready["amount"]) > int(best_swap[0]["amount"]):
        best_swap[0] = ready

print(best_swap)

end = datetime.now()
print("duration of program is {}".format(end - start))
