""" Use this script if you have multiple wallets, and have closed ETH-USDC 
positions in each wallet.
"""

from dataprep import load_n_prep_data

# --- BEGIN Input --- #

wallet_names = ['wallet1', 'wallet2',]
pair = 'ETH-USDC'

# --- END Input --- #

# constant 
COLS = [
    'nft_id', 'open_datetime', 'close_datetime', 'duration_days',
    'sent_eth', 'sent_usdc', 'withdrawn_eth', 'withdrawn_usdc', 
    'lp_delta_eth', 'lp_delta_usdc', 
    'fees_eth', 'fees_usdc', 'gas_eth', 'pnl_eth', 'pnl_usdc', 
    'investment_opentime_usd_value', 
    'pnl_closetime_usd_value', 'investment_closetime_usd_value', 
    'closetime_APR', 'closetime_daily_PnL', 
    'pnl_current_usd_value', 'investment_current_usd_value', 
    'current_APR', 'current_daily_PnL',
]

# load and clean data
for wallet_name in wallet_names:
    df = load_n_prep_data(wallet_name, pair) 
    # re-order the columns and write out csv file
    csv_fname = f'../data/cleaned-arbi-univ3lp-perf-{wallet_name}-{pair}.csv'
    df[COLS].to_csv(csv_fname, index=False)

