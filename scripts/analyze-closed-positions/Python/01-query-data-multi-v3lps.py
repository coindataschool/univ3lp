""" Run this script if you have multiple closed positions of the same Uniswap 
V3 LP pair on Arbitrum. It pulls their performance metrics from dune analytics, 
and saves them in a csv file in the /data folder. If a file already exists, it 
will just appened the new records to the file. 
"""

import os
import pandas as pd # needed for dune.refresh_into_dataframe() to work
from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import Query

# --- BEGIN Input --- #

pair = 'ETH-USDC'           # v3 LP pair on Arbitrum. The right coin should 
    # always be USDC, USDT, or ETH, and the left coin should always be a 
    # volatile coin. For example, 'ETH-USDC' is valid but 'USDC-ETH' is not;
    # 'ARB-USDT' is valid but 'USDT-ARB' is not;
    # 'ARB-ETH' is valid but 'ETH-ARB' is not. 
wallet_name = 'wallet1'     # name of your wallet
nft_ids = [489349, 586698,] # a list of V3 NFT ids of your closed positions

# --- END Input --- #

# create folder to store downloaded data
data_dir = '../data'
os.makedirs(data_dir, exist_ok=True)

# look up query id based on pair
if pair == 'ETH-USDC':
    qid = 2331962
elif pair == 'ETH-USDT':
    qid = 2449148
elif pair == 'STG-ETH':
    qid = 2438599
elif pair == 'GMX-USDC':
    qid = 2394629
elif pair == 'GMX-ETH':
    qid = 2394607
elif pair == 'ARB-ETH':
    qid = 2372846
elif pair == 'ARB-USDT':
    qid = 2372824
elif pair == 'ARB-USDC':
    qid = 2372781
elif pair == 'MCB-ETH':
    qid = 2449102
elif pair == 'MCB-USDC':    
    qid = 2449112    
else:
    qid = None

if qid:
    # get your api key from dune, save and export it in .zshrc or .bashrc
    dune = DuneClient(os.environ["DUNE_API_KEY"]) 

    lst_of_dfs = []
    for nft_id in nft_ids:    
        query = Query(
            name="Univ3 LP Performance Query",
            query_id=qid,
            params=[
                QueryParameter.number_type(
                    name=f"Arbitrum UniV3 {pair} LP NFT id", value=nft_id),
            ],
        )
        # print("Results available at", query.url())
        # results = dune.refresh_csv(query)
        df = dune.refresh_into_dataframe(query)
        lst_of_dfs.append(df)
    # stack into one frame and save as csv
    df = pd.concat(lst_of_dfs)
    fname = f'arbi-univ3lp-perf-{wallet_name}-{pair}.csv'
    fpath = os.path.join(data_dir, fname)
    if os.path.exists(fpath):
        pd.concat([pd.read_csv(fpath), df]).to_csv(fpath, index=False)
    else:
        df.to_csv(fpath, index=False)

