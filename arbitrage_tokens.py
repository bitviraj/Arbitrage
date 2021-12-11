import requests
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

"""wallet = os.getenv("wallet")
bsc = os.getenv("BSC")
w3 = Web3(Web3.HTTPProvider(bsc))

balance = w3.eth.get_balance(wallet)

baalnce = w3.fromWei(balance, "ether")
print(balance)"""


response_tokens = requests.get(os.getenv("url_tokens"))

tokens = response_tokens.json()["tokens"]

token_address = []
for token in tokens:
    token_address.append(token)
