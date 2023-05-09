import pandas as pd
from dataprep import load_n_prep_data
import pickle

# --- BEGIN Input --- #

wallet_name = 'wallet2'
pairs = ['MCB-USDC', 'MCB-ETH',]  # if you don't have one of the
    # pairs in your closed position, remove it from the list and remove the 
    # corresponding columns in the `COLS` list below.

# --- END Input --- #

# load and clean data
with open('../data/current_prices.pickle', 'rb') as handle:
    prices = pickle.load(handle)
current_eth_price = prices.loc[prices['symbol'] == 'WETH', 'price'][0]
current_mcb_price = prices.loc[prices['symbol'] == 'MCB', 'price'][0]
df = pd.concat([
    load_n_prep_data(wallet_name, pair, current_eth_price, current_mcb_price) 
    for pair in pairs
]).fillna(0)

# re-order the columns and write out csv file
COLS = [
    'nft_id', 'open_datetime', 'close_datetime', 'duration_days',
    'sent_mcb', 'sent_eth', 'sent_usdc', 
    'withdrawn_mcb', 'withdrawn_eth', 'withdrawn_usdc', 
    'lp_delta_mcb', 'lp_delta_eth', 'lp_delta_usdc', 
    'fees_mcb', 'fees_eth', 'fees_usdc', 
    'gas_eth', 'pnl_mcb', 'pnl_eth', 'pnl_usdc', 
    'investment_opentime_usd_value', 
    'pnl_closetime_usd_value', 'investment_closetime_usd_value', 
    'closetime_APR', 'closetime_daily_PnL', 
    'pnl_current_usd_value', 'investment_current_usd_value', 
    'current_APR', 'current_daily_PnL',
]
coin = pairs[0].split('-')[0]
csv_fname = f'../data/cleaned-arbi-univ3lp-perf-{wallet_name}-{coin}-pairs.csv'
df[COLS].to_csv(csv_fname, index=False)
