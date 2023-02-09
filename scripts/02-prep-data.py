import numpy as np
import pandas as pd
import json
import os

def prep_data(raw_data):
    # Process raw data.
    #
    # raw_data: a list of data dictionary 

    lst_dfs_curr = []
    lst_dfs_hist = []    
    for i in range(len(raw_data)):
        if i % 100 == 0:
            print("Processed {} univ3 LP positions".format(i))
        dct = raw_data[i]
        # extract profile info and current PnLs and APRs
        row_base = pd.DataFrame({k:v for k, v in dct.items() if type(v) in [str, bool, float, int]}, index=range(1))
        row_perf = pd.DataFrame(dct['performance']['hodl'], index=range(1))
        row_chng = pd.DataFrame(dct['deltas_24h'], index=range(1))
        row_chng.columns = 'delta24h_' + row_chng.columns
        row = pd.concat([row_base, row_perf, row_chng], axis=1).drop(columns=['network', 'exchange'])
        lst_dfs_curr.append(row)
                
        # extract historical PnLs and APRs
        da = pd.DataFrame(dct['history_24h'])
        da['nft_id'] = row['nft_id'][0]
        da = da[['nft_id', 'ts', 'pnl', 'apr', 'fee_apr']]
        lst_dfs_hist.append(da)
            
        # # extract historical compounding cashflows
        # pd.DataFrame(dct['cash_flows'])
        
    df_curr = pd.concat(lst_dfs_curr).set_index('nft_id')
    df_hist = pd.concat(lst_dfs_hist).set_index('nft_id')
    
    # clean current data
    bool_vars = [col for col in df_curr.columns if df_curr[col].dtype == 'bool']
    int_vars = [col for col in df_curr.columns if df_curr[col].dtype == 'int']
    float_vars = [col for col in df_curr.columns if df_curr[col].dtype == 'float']
    char_vars = ['pool', 'token0', 'token1', 'og_owner', 'real_owner', 'owner']

    other_vars = df_curr.columns[~df_curr.columns.isin(char_vars+float_vars+int_vars+bool_vars)]
    for col in other_vars:    
        df_curr[col] = df_curr[col].replace('', np.nan).astype(float)
    
    # clean historical data
    df_hist = df_hist.replace('', np.nan)
    df_hist['ts'] = df_hist['ts'].astype(int)
    df_hist['pnl'] = df_hist['pnl'].astype(float)
    df_hist['apr'] = df_hist['apr'].astype(float)
    df_hist['fee_apr'] = df_hist['fee_apr'].astype(float) 
    df_hist = df_hist.dropna(thresh=2)
    
    print('All Done!\n')
    return {'current': df_curr, 'historical': df_hist}

if __name__ == "__main__":
    for chain in ['mainnet', 'arbitrum']:
        # chain = 'arbitrum'
        fnms = ['../data/data_{}-v1.json'.format(chain),
                '../data/data_{}.json'.format(chain)]
        lst_curr = []; lst_hist = []
        for fnm in fnms:
            if os.path.isfile(fnm):
                print('Blockchain:', chain)
                with open(fnm, 'r') as f:
                    raw_data = json.load(f)['data']
                dd = prep_data(raw_data)
                lst_curr.append(dd['current'])
                lst_hist.append(dd['historical'])
        df_curr = pd.concat(lst_curr).drop_duplicates()
        df_hist = pd.concat(lst_hist).drop_duplicates()
        pd.to_pickle(df_curr, '../data/univ3_{}_lps.pkl'.format(chain))
        pd.to_pickle(df_hist, '../data/univ3_{}_lps_hist_perf.pkl'.format(chain))
