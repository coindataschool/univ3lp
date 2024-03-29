from dataprep import aggregate_ethStable_altStable_altEth
import pickle

# --- BEGIN Input --- #

wallet_name = 'wallet2'
pair = 'MCB-pairs'
capital_mcb = 0             # How many GMX did you use to LP?
capital_eth = 0             # How many ETH did you use to LP?
capital_usdc = 1000         # How many USDC did you use to LP?
capital_usdt = 0            # How many USDT did you use to LP?
transfer_cost_usdc = -(0)   # non-positive, cost of on-ramp, stargate transfer
transfer_cost_usdt = -(0)   # non-positive, cost of on-ramp, stargate transfer
transfer_gas_eth = -(0)     # non-positive, gas on transfer starting and arrival chains
approve_gas_eth = -(0)      # non-positive, gas for token approval 
failed_mint_gas_eth = -(0)  # non-positive, gas for failed LP tx

# --- END Input --- #

# load current prices
with open('../data/current_prices.pickle', 'rb') as handle:
    prices = pickle.load(handle)
current_eth_price = prices.loc[prices['symbol'] == 'WETH', 'price'][0]
current_mcb_price = prices.loc[prices['symbol'] == 'MCB', 'price'][0]

# main
transfer_cost_usd = transfer_cost_usdc + transfer_cost_usdt
other_gas_eth = transfer_gas_eth + approve_gas_eth + failed_mint_gas_eth
aggregate_ethStable_altStable_altEth(
    wallet_name, pair, transfer_cost_usd, other_gas_eth, 
    capital_eth, capital_usdc, capital_usdt=0, capital_alt=capital_mcb, current_eth_price=current_eth_price, current_alt_price=current_mcb_price
)