import pandas as pd
import pickle 
import os

# input 
capital_reused = 1000 # capital re-used in different LP pairs. For example,
    # you may use $1000 USDC in a single-sided ETH-USDC position, and say price
    # takes a round-trip and you get back your $1000 USDC after closure, and 
    # you deploy the same $1000 USDC in a GMX-USDC pool. This $1000 USDC will
    # be considered as re-used. Even if there's no round trip, say your $1000 
    # USDC gets all converted to ETH, and you close and take the ETH and deploy 
    # to the ARB-ETH pool, your $1000 USDC capital will still be re-used.

# read data
data_dir = '../data'
lst = []
for name in os.listdir(data_dir):
    if name.endswith('.pickle') and name != 'current_prices.pickle':
        with open(os.path.join(data_dir, name), 'rb') as handle:
            lst.append(pickle.load(handle))
df = pd.concat(lst).sort_values('daily_fees', ascending=False)
df.to_csv(os.path.join(data_dir, 'final-aggregate-all.csv'), index=False)

# print key metrics on screen
timediff = df['stop_time'].max() - df['start_time'].min()
dur_days = timediff.days + timediff.seconds/3600/24
positions = df['closed_position_cnt'].sum()
fees_less_gas = df['total_fees_less_gas'].sum()
pnl = df['total_pnl'].sum()
capital = df['capital'].sum() - capital_reused # remove multiple counting of 
    # the same capital
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
