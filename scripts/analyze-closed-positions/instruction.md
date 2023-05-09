# How to Run the Scripts

1. Change the input section of `01-query-data-multi-v3lps.py` (or `01-query-data-one-v3lp.py`). Run it in terminal. This will download the performance metrics of your closed univ3 LP position and save them under `/data`.
    - `python 01-query-data-multi-v3lps.py`
    - `python 01-query-data-one-v3lp.py`
2. Pull current prices from DeFiLlama. The prices will be saved under `/data`.
    - `python 02-get-current-prices.py`
    ![](https://github.com/coindataschool/univ3lp/blob/main/scripts/analyze-closed-positions/screens/print-out-02-get-current-prices.png)
3. Change the input section of the `03-clean-data-XXX-pairs.py` scripts and run them. This will clean up
the performance metrics and save the outout under `/data`.
    - `python 03-clean-data-ARB-pairs.py`
    - `python 03-clean-data-ETH-pairs.py`
    - `python 03-clean-data-GMX-pairs.py`
    - `python 03-clean-data-MCB-pairs.py`
    - `python 03-clean-data-STG-pairs.py`
1. Aggregate across all closed positions of the same volatile coin under the same wallet.
    - `python 04-aggregate-ARB-pairs.py`
    ![](https://github.com/coindataschool/univ3lp/blob/main/scripts/analyze-closed-positions/screens/print-out-04-aggregate-ARB-pairs.png)
    - `python 04-aggregate-ETH-pairs.py`
    ![](https://github.com/coindataschool/univ3lp/blob/main/scripts/analyze-closed-positions/screens/print-out-04-aggregate-ETH-pairs.png)
    - `python 04-aggregate-GMX-pairs.py`
    ![](https://github.com/coindataschool/univ3lp/blob/main/scripts/analyze-closed-positions/screens/print-out-04-aggregate-GMX-pairs.png)
    - `python 04-aggregate-MCB-pairs.py`
    ![](https://github.com/coindataschool/univ3lp/blob/main/scripts/analyze-closed-positions/screens/print-out-04-aggregate-MCB-pairs.png)
    - `python 04-aggregate-STG-pairs.py`
    ![](https://github.com/coindataschool/univ3lp/blob/main/scripts/analyze-closed-positions/screens/print-out-04-aggregate-STG-pairs.png)
2. Aggregate across all wallets and output a `final-aggregate-all.csv` file under `/data`.
    - `python 05-aggregate-all.py`
    ![](https://github.com/coindataschool/univ3lp/blob/main/scripts/analyze-closed-positions/screens/print-out-05-aggregate-all.png)