# download Univ3 positions from revert finance
# script credit: https://github.com/0x1egolas/crypto-scripts/blob/main/pull-revert-finance.py

import requests
import json
import traceback
import os 

def run(chain):
    params = {
        'sort': 'apr',
        'page': 0,
        'desc': True,
        'limit': 100,
        'offset': 0,
        # 'active': True # doesn't seem to do anything
    }
    url = 'https://staging-api.revert.finance/v1/positions/{}/uniswapv3'.format(chain)
    data = []
    while True:
        if params['page'] % 5 == 0:
            print(f"getting page {params['page']}")
        try:
            res = requests.get(url, params)
        except:
            print(traceback.format_exc())
            break
        data.extend(res.json()['data'])
        params['page'] += 1
        params['offset'] += params['limit']
        if params['offset'] > res.json()['total_count']:
            break
    os.makedirs('../data', exist_ok=True)
    with open('../data/data_{}.json'.format(chain), 'w+') as f:
        f.write(json.dumps({'data': data}))    
    # data_type = 'active' if params['active'] else 'inactive'
    # with open('../data/{}_data_{}.json'.format(data_type, chain), 'w+') as f:
    #     f.write(json.dumps({'data': data}))

if __name__ == "__main__":
    run('mainnet')
    # run('arbitrum')