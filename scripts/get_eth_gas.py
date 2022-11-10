import json
from web3 import Web3
import requests
import os 

alchemy_api_key = os.environ.get('ALCHEMY_API_KEY') # replace with your own api key, and you can get one at https://www.alchemy.com/
node_url = "https://eth-mainnet.g.alchemy.com/v2/"+alchemy_api_key

# get gas from ethereum block chain
w3 = Web3(Web3.HTTPProvider(node_url))
eth_gas_price = w3.eth.gasPrice
print("From alchemy node:")
print('- baseFee', eth_gas_price/1e9)  # -> gwei

# get gas from Etherscan's gas tracker
# https://etherscan.io/gastracker
req = requests.get('https://api.etherscan.io/api?module=gastracker&action=gasoracle')
t = json.loads(req.content)['result']
print("From Etherscan Gas Tracker:")
print('- safeLow', t['SafeGasPrice'])
print('- proposed', t['ProposeGasPrice'])
print('- fast', t['FastGasPrice'])
print('- baseFee', t['suggestBaseFee'], end='\n\n')