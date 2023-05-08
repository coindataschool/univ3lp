from prices import current_arb_price
from dataprep import aggregate_ethStable_altStable_altEth

# --- BEGIN Input --- #

wallet_name = 'wallet1'
pair = 'ARB-pairs'
capital_arb = 10000          # How many ARB did you use to LP?
capital_eth = 0              # How many ETH did you use to LP?
capital_usdc = 0             # How many USDC did you use to LP?
capital_usdt = 0             # How many USDT did you use to LP?
transfer_cost_usdc = -(0)    # non-positive, cost of on-ramp, stargate transfer
transfer_cost_usdt = -(0)    # non-positive, cost of on-ramp, stargate transfer
approve_gas_eth = -(0)       # non-positive, gas for token approval 
failed_mint_gas_eth = -(0)   # non-positive, gas for failed LP tx
airdrop_claim_gas_eth = -(0) # non-positive, gas for airdrop claim

# --- END Input --- #


# main
transfer_cost_usd = transfer_cost_usdc + transfer_cost_usdt
other_gas_eth = approve_gas_eth + failed_mint_gas_eth + airdrop_claim_gas_eth
aggregate_ethStable_altStable_altEth(
    wallet_name, pair, transfer_cost_usd, other_gas_eth, 
    capital_eth, capital_usdc, capital_usdt, 
    capital_alt=capital_arb, current_alt_price=current_arb_price
)