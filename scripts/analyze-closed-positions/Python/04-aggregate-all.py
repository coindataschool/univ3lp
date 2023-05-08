import pandas as pd
import pickle 
import os

data_dir = '../data'
lst = []
for name in os.listdir(data_dir):
    if name.endswith('.pickle'):
        with open(os.path.join(data_dir, name), 'rb') as handle:
            lst.append(pickle.load(handle))
df = pd.concat(lst)
df.to_csv(os.path.join(data_dir, 'final-aggregate-all.csv'), index=False)

# print key metrics on screen
timediff = df['stop_time'].max() - df['start_time'].min()
dur_days = timediff.days + timediff.seconds/3600/24
positions = df['closed_position_cnt'].sum()
fees_less_gas = df['total_fees_less_gas'].sum()
pnl = df['total_pnl'].sum()
capital = df['capital'].sum() - 2496.93*2 
print("Duration:", '{:.2f} days'.format(dur_days))
print('At Current Prices,')
print('  - Total Capital:', '${:.2f}'.format(capital)) 
print('  - Total Net Earnings:', '${:.2f}'.format(fees_less_gas)) 
print('  - Total PnL:', '${:.2f}'.format(pnl))
daily_fees = fees_less_gas / dur_days
daily_pnl = pnl / dur_days
print('  - Daily Net Earnings:', '${:.2f}'.format(daily_fees))
print('  - Daily PnL:', '${:.2f}'.format(daily_pnl))
fee_apr = fees_less_gas / capital / dur_days * 365
tot_apr = pnl / capital / dur_days * 365
print('  - Fee APR:', '{:.2f}%'.format(fee_apr*100))
print('  - Total APR:', '{:.2f}%'.format(tot_apr*100))
est_annual_fees = daily_fees * 365
est_annual_pnl = daily_pnl * 365
print('  - Estimated Annual Net Earnings:', '${:.2f}'.format(est_annual_fees))
print('  - Estimated Annual PnL:', '${:.2f}'.format(est_annual_pnl))
