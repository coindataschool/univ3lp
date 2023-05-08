from dataprep import load_n_prep_data

# --- BEGIN Input --- #

wallet_name = 'wallet1'
pair = 'STG-ETH'

# --- END Input --- #

# constant 
COLS = [
    'nft_id', 'open_datetime', 'close_datetime', 'duration_days',
    'sent_stg', 'sent_eth', 'withdrawn_stg', 'withdrawn_eth', 
    'lp_delta_stg', 'lp_delta_eth', 
    'fees_stg', 'fees_eth', 'gas_eth', 'pnl_stg', 'pnl_eth', 
    'investment_opentime_usd_value', 
    'pnl_closetime_usd_value', 'investment_closetime_usd_value', 
    'closetime_APR', 'closetime_daily_PnL', 
    'pnl_current_usd_value', 'investment_current_usd_value', 
    'current_APR', 'current_daily_PnL',
]

# load and clean data
df = load_n_prep_data(wallet_name, pair) 
# re-order the columns and write out csv file
csv_fname = f'../data/cleaned-arbi-univ3lp-perf-{wallet_name}-{pair}.csv'
df[COLS].to_csv(csv_fname, index=False)
