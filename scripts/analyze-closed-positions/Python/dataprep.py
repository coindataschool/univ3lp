import pandas as pd
from prices import current_eth_price, current_arb_price, current_stg_price
from prices import current_gmx_price, current_mcb_price
import pickle 

def load_n_prep_data(wallet, pair):
    """Read data, drop useless cols and add new cols. 
    """
    fname = f'../data/arbi-univ3lp-perf-{wallet}-{pair}.csv'
    df = pd.read_csv(fname, parse_dates=['open_datetime', 'close_datetime'], 
                     infer_datetime_format=True)
    # drop useless cols
    df = df.loc[:, ~df.columns.str.contains('current|ROI|price')]
    # add metrics at current prices
    if pair == 'ARB-USDC':
        df['pnl_current_usd_value'] =\
            current_arb_price * df['pnl_arb']\
            + current_eth_price * df['pnl_eth']\
            + df['pnl_usdc']    
        df['investment_current_usd_value'] =\
            current_arb_price * df['sent_arb'] + df['sent_usdc']
    if pair == 'ARB-USDT':
        df['pnl_current_usd_value'] =\
            current_arb_price * df['pnl_arb']\
            + current_eth_price * df['pnl_eth']\
            + df['pnl_usdt']    
        df['investment_current_usd_value'] =\
            current_arb_price * df['sent_arb'] + df['sent_usdt']
    if pair == 'ARB-ETH':
        df['pnl_current_usd_value'] =\
            current_arb_price * df['pnl_arb']\
            + current_eth_price * df['pnl_eth']    
        df['investment_current_usd_value'] =\
            current_arb_price * df['sent_arb']\
            + current_eth_price * df['sent_eth']
    if pair == 'ETH-USDC':
        df['pnl_current_usd_value'] =\
            current_eth_price * df['pnl_eth'] + df['pnl_usdc']
        df['investment_current_usd_value'] =\
            current_eth_price * df['sent_eth'] + df['sent_usdc']            
    if pair == 'STG-ETH':
        df['pnl_current_usd_value'] =\
            current_eth_price * df['pnl_eth']\
            + current_stg_price * df['pnl_stg']    
        df['investment_current_usd_value'] = \
            current_eth_price * df['sent_eth']\
            + current_stg_price * df['sent_stg']
    if pair == 'GMX-ETH':
        df['pnl_current_usd_value'] =\
            current_eth_price * df['pnl_eth']\
            + current_gmx_price * df['pnl_gmx']
        df['investment_current_usd_value'] =\
            current_eth_price * df['sent_eth']\
            + current_gmx_price * df['sent_gmx']
    if pair == 'GMX-USDC':
        df['pnl_current_usd_value'] =\
            current_gmx_price * df['pnl_gmx']\
            + current_eth_price * df['pnl_eth']\
            + df['pnl_usdc']
        df['investment_current_usd_value'] = \
            current_gmx_price * df['sent_gmx'] + df['sent_usdc']
    if pair == 'MCB-ETH':
        df['pnl_current_usd_value'] =\
            current_eth_price * df['pnl_eth']\
            + current_mcb_price * df['pnl_mcb']
        df['investment_current_usd_value'] =\
            current_eth_price * df['sent_eth']\
            + current_mcb_price * df['sent_mcb']
    if pair == 'MCB-USDC':
        df['pnl_current_usd_value'] =\
            current_mcb_price * df['pnl_mcb']\
            + current_eth_price * df['pnl_eth']\
            + df['pnl_usdc']
        df['investment_current_usd_value'] = \
            current_mcb_price * df['sent_mcb'] + df['sent_usdc']
            
    roi = df['pnl_current_usd_value'] / df['investment_current_usd_value']
    df['current_APR'] = roi / df['duration_days'] * 365
    df['current_daily_PnL'] =\
        df['pnl_current_usd_value'] / df['duration_days']
    return df


def aggregate_ethStable_altStable_altEth(
    wallet_name, pair, transfer_cost_usd, uncaptured_gas_eth, capital_eth, 
    capital_usdc, capital_usdt, capital_alt=0, current_alt_price=0):
    """ Aggregates Fees (less gas paid in eth and transfer fees paid in 
    stablecoin, for example, when sending USDC/USDT from Polygon to Arbitrum 
    via stargate) and PnLs of all closed eth-stable, alt-stablecoin, and alt-eth
    positions in a wallet, where alt is any non-ETH volatile token and 
    stablecoin is either USDC or USDT.
    
    uncaptured_gas_eth: gas for contract approve, failed mint, airdrop claim
        and etc. 
    """
    # load performance data
    perf_fname = f'../data/cleaned-arbi-univ3lp-perf-{wallet_name}-{pair}.csv'
    df = pd.read_csv(perf_fname, 
                     parse_dates=['open_datetime', 'close_datetime'], 
                     infer_datetime_format=True)
    print('Wallet:', wallet_name)
    print('Pair:', pair, f'({df.shape[0]} closed positions)')

    # extract alt coin symbol and construct fee colnames
    alt_coin = pair.split('-')[0]
    fees_col_alt = 'fees_' + alt_coin.lower()
    fees_col_eth = 'fees_eth'
    fees_col_usdc = 'fees_usdc'
    fees_col_usdt = 'fees_usdt'

    # aggregate fees (less gas or transfer fees paid in usd) over all positions
    if alt_coin == 'ETH':
        fees = df[fees_col_eth].sum() * current_eth_price
    else: 
        fees = df[fees_col_alt].sum() * current_alt_price
        if fees_col_eth in df.columns:
            fees += df[fees_col_eth].sum() * current_eth_price
    if fees_col_usdc in df.columns:
        fees += df[fees_col_usdc].sum()
    if fees_col_usdt in df.columns:
        fees += df[fees_col_usdt].sum()
    gas = (df['gas_eth'].sum() + uncaptured_gas_eth) * current_eth_price\
        + transfer_cost_usd 
    fees_less_gas = fees + gas # gas is already negative
    # aggregate pnl over all positions
    pnl = df['pnl_current_usd_value'].sum()\
        + uncaptured_gas_eth * current_eth_price\
        + transfer_cost_usd
    # calc duration in days
    timediff = df['close_datetime'].max() - df['open_datetime'].min()
    dur_days = timediff.days + timediff.seconds/3600/24
    print("Duration:", '{:.2f} days'.format(dur_days))
    print('At Current Prices,')
    print('  - Total Fees less Gas:', '${:.2f}'.format(fees_less_gas)) 
    print('  - Total PnL:', '${:.2f}'.format(pnl))

    # calc fee APR, total APR, daily fees, and daily PnL
    if alt_coin == 'ETH':
        capital = current_eth_price * capital_eth\
            + capital_usdc + capital_usdt
    else:
        capital = current_alt_price * capital_alt\
            + current_eth_price * capital_eth\
            + capital_usdc + capital_usdt
    fee_apr = fees_less_gas / capital / dur_days * 365
    tot_apr = pnl / capital / dur_days * 365
    print('  - Fee APR:', '{:.2f}%'.format(fee_apr*100))
    print('  - Total APR:', '{:.2f}%'.format(tot_apr*100))
    daily_fees = fees_less_gas / dur_days
    daily_pnl = pnl / dur_days
    print('  - Daily Fees:', '${:.2f}'.format(daily_fees))
    print('  - Daily PnL:', '${:.2f}'.format(daily_pnl))

    # save aggregated metrics   
    row = pd.DataFrame({
        "wallet": wallet_name,
        "pair": pair,
        "capital": capital,
        "start_time": df['open_datetime'].min(), 
        "stop_time": df['close_datetime'].max(),
        "duration": dur_days,
        "closed_position_cnt": df.shape[0],    
        "total_fees_less_gas": fees_less_gas,
        "total_pnl": pnl,
        "fee_apr": fee_apr,
        "total_apr": tot_apr, 
        "daily_fees": daily_fees,
        "daily_pnl": daily_pnl
        }, index=range(1))
    save_fname = perf_fname.replace('cleaned', 'totaled')\
        .replace('.csv', '.pickle')
    with open(save_fname, 'wb') as handle:
        pickle.dump(row, handle, -1)