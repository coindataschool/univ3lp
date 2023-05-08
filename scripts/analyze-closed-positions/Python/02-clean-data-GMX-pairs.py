import pandas as pd 
from dataprep import load_n_prep_data

# --- BEGIN Input --- #

wallet_name = 'wallet1'
pairs = ['GMX-USDC', 'GMX-ETH'] # if you don't have one of the
    # pairs in your closed position, remove it from the list and remove the 
    # corresponding columns in the `COLS` list below.

# --- END Input --- #

# load and clean data
df = pd.concat([load_n_prep_data(wallet_name, pair) for pair in pairs])\
       .fillna(0)

# re-order the columns and write out csv file
COLS = [
    'nft_id', 'open_datetime', 'close_datetime', 'duration_days',
    'sent_gmx', 'sent_eth', 'sent_usdc', 
    'withdrawn_gmx', 'withdrawn_eth', 'withdrawn_usdc', 
    'lp_delta_gmx', 'lp_delta_eth', 'lp_delta_usdc', 
    'fees_gmx', 'fees_eth', 'fees_usdc', 'gas_eth',
    'pnl_gmx', 'pnl_eth', 'pnl_usdc', 
    'investment_opentime_usd_value', 
    'pnl_closetime_usd_value', 'investment_closetime_usd_value', 
    'closetime_APR', 'closetime_daily_PnL', 
    'pnl_current_usd_value', 'investment_current_usd_value', 
    'current_APR', 'current_daily_PnL',
]
coin = pairs[0].split('-')[0]
csv_fname = f'../data/cleaned-arbi-univ3lp-perf-{wallet_name}-{coin}-pairs.csv'
df[COLS].to_csv(csv_fname, index=False)