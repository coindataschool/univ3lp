""" Use this script if you have multiple wallets, and have closed ETH-USDC and 
ETH-USDT positions in each wallet.
"""
import pandas as pd
from dataprep import load_n_prep_data

# --- BEGIN Input --- #

wallet_names = ['wallet1', 'wallet2',] 
pairs = ['ETH-USDC', 'ETH-USDT'] 

# --- END Input --- #

# constant 
COLS = [
    'nft_id', 'open_datetime', 'close_datetime', 'duration_days',
    'sent_eth', 'sent_usdc', 'sent_usdt', 
    'withdrawn_eth', 'withdrawn_usdc', 'withdrawn_usdt', 
    'lp_delta_eth', 'lp_delta_usdc', 'lp_delta_usdt', 
    'fees_eth', 'fees_usdc', 'fees_usdt',
    'gas_eth', 'pnl_eth', 'pnl_usdc', 'pnl_usdt', 
    'investment_opentime_usd_value', 'pnl_closetime_usd_value', 
    'investment_closetime_usd_value', 'closetime_APR', 'closetime_daily_PnL', 
    'pnl_current_usd_value', 'investment_current_usd_value', 
    'current_APR', 'current_daily_PnL',
]

# load and clean data
coin = pairs[0].split('-')[0]
for wallet_name in wallet_names:
    df = pd.concat([load_n_prep_data(wallet_name, pair) for pair in pairs])\
           .fillna(0)
    # re-order the columns and write out csv file
    csv_fname = f'../data/cleaned-arbi-univ3lp-perf-{wallet_name}-{coin}-pairs.csv'
    df[COLS].to_csv(csv_fname, index=False)

