from defillama2 import DefiLlama
import pickle 

# download current prices via DeFiLlama's API
obj = DefiLlama()
dd = {
    '0x82aF49447D8a07e3bd95BD0d56f35241523fBab1':'arbitrum', # WETH
    '0x912CE59144191C1204E64559FE8253a0e49E6548':'arbitrum', # ARB
    '0xfc5A1A6EB076a2C7aD06eD22C90d7E710E35ad0a':'arbitrum', # GMX
    '0x6694340fc020c5E6B96567843da2df01b2CE1eb6':'arbitrum', # STG
    '0x4e352cF164E64ADCBad318C3a1e222E9EBa4Ce42':'arbitrum', # MCB
}
prices = obj.get_tokens_curr_prices(dd)
with open('../data/current_prices.pickle', 'wb') as handle:
    pickle.dump(prices, handle, -1)
    
# extract prices
current_eth_price = prices.loc[prices['symbol'] == 'WETH', 'price'][0]
current_arb_price = prices.loc[prices['symbol'] == 'ARB', 'price'][0]
current_stg_price = prices.loc[prices['symbol'] == 'STG', 'price'][0]
current_gmx_price = prices.loc[prices['symbol'] == 'GMX', 'price'][0]
current_mcb_price = prices.loc[prices['symbol'] == 'MCB', 'price'][0]
print('Current ETH Price:', current_eth_price)
print('Current ARB Price:', current_arb_price)
print('Current STG Price:', current_stg_price)
print('Current GMX Price:', current_gmx_price)
print('Current MCB Price:', current_mcb_price)
    