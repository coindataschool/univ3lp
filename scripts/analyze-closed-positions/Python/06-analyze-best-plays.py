import pandas as pd
import os
import dataframe_image as dfi 

# input 
coins = ['ARB', 'ETH'] # , 'GMX', 'MCB', 'STG'
sortby_vars = ['closetime_APR', 'pnl_closetime_usd_value']

# set paths
data_dir = '../data'
png_dir = '../png'
os.makedirs(png_dir, exist_ok=True)

for sortby_var in sortby_vars:
    for coin in coins:
        # read data
        lst = []
        for fname in os.listdir(data_dir):
            if fname.endswith(f'{coin}-pairs.csv') and fname.startswith('cleaned-arbi-univ3lp'):
                fpath = os.path.join(data_dir, fname)
                lst.append(
                    pd.read_csv(fpath, 
                                parse_dates=['open_datetime', 'close_datetime'], 
                                infer_datetime_format=True)
                    )
        df = pd.concat(lst).sort_values(sortby_var, ascending=False)

        # find top 10 positions by closetime APR with >=$10 PnL at closing time
        # cond = (df.columns.str.startswith('sent_') | 
        #         df.columns.str.startswith('withdrawn_'))
        # cols = df.columns[cond].to_list()
        cols = ['investment_opentime_usd_value',
                'duration_days',
                'closetime_APR',
                'current_APR',
                'investment_closetime_usd_value',
                'investment_current_usd_value',
                'pnl_closetime_usd_value',
                'pnl_current_usd_value',]
        df_top10 = df.loc[df['pnl_closetime_usd_value']>=10, cols]\
            .head(10).reset_index(drop=True)

        # print out 
        format_dict = {
            'investment_opentime_usd_value': '${:,.0f}',
            'duration_days': '{:,.3f}',
            'closetime_APR': '{:.0%}',
            'current_APR': '{:.0%}', 
            'investment_closetime_usd_value': '${:,.0f}',
            'investment_current_usd_value': '${:,.0f}',
            'pnl_closetime_usd_value': '${:,.2f}',
            'pnl_current_usd_value': '${:,.2f}',
            }
        df_styled = df_top10.style.format(format_dict)
        tmp_var = sortby_var.replace('_usd_value', '').replace('_', '-')
        fname = f'top10-by-{tmp_var}-{coin}-pairs.png'
        dfi.export(df_styled, os.path.join(png_dir, fname))
