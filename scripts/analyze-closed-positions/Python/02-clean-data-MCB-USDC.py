import pandas as pd 
from dataprep import load_n_prep_data

# --- BEGIN Input --- #

wallet_name = 'wallet1'
pair = 'MCB-USDC'

# --- END Input --- #

# load and clean data
df = load_n_prep_data(wallet_name, pair).fillna(0)

# re-order the columns and write out csv file
COLS = [
    'nft_id', 'open_datetime', 'close_datetime', 'duration_days',
    'sent_mcb', 'sent_usdc', 
    'withdrawn_mcb', 'withdrawn_usdc', 
    'lp_delta_mcb', 'lp_delta_usdc', 
    'fees_mcb', 'fees_usdc', 'gas_eth',
    'pnl_mcb', 'pnl_eth', 'pnl_usdc', 
    'investment_opentime_usd_value', 
    'pnl_closetime_usd_value', 'investment_closetime_usd_value', 
    'closetime_APR', 'closetime_daily_PnL', 
    'pnl_current_usd_value', 'investment_current_usd_value', 
    'current_APR', 'current_daily_PnL',
]
coin = pair.split('-')[0]
csv_fname = f'../data/cleaned-arbi-univ3lp-perf-{wallet_name}-{pair}.csv'
df[COLS].to_csv(csv_fname, index=False)
