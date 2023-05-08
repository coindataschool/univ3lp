from prices import current_stg_price
from dataprep import aggregate_ethStable_altStable_altEth

# --- BEGIN Input --- #

wallet_name = 'wallet1'
pair = 'STG-ETH'
capital_stg = 0         # How many STG did you use to LP?
capital_eth = 1         # How many ETH did you use to LP?
capital_usdc = 0        # How many USDC did you use to LP?
capital_usdt = 0        # How many USDT did you use to LP?
transfer_cost_usdc = -(0)   # non-positive, cost of on-ramp, stargate transfer
transfer_cost_usdt = -(0)   # non-positive, cost of on-ramp, stargate transfer
approve_gas_eth = -(0)      # non-positive, gas for token approval 
failed_mint_gas_eth = -(0)  # non-positive, gas for failed LP tx

# --- END Input --- #

# main
transfer_cost_usd = transfer_cost_usdc + transfer_cost_usdt
other_gas_eth = approve_gas_eth + failed_mint_gas_eth
aggregate_ethStable_altStable_altEth(
    wallet_name, pair, transfer_cost_usd, other_gas_eth, 
    capital_eth, capital_usdc, capital_usdt, 
    capital_alt=capital_stg, current_alt_price=current_stg_price
)