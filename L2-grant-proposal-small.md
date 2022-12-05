# Analyze Uniswap V3 LP Positions Data on Mainnet and Arbitrum

* **Project Name:** Analyze Uniswap V3 LP Positions Data on Mainnet and Arbitrum
* **Team Name:** Coin Data School

## Project Overview

We'd like to gather, visualize, and analyze mainnet and arbitrum UniV3
LP positions data to uncover LP behavior patterns, and predict ROI and fee APR
with machine learning. The goal is to study the difference (and commonality) in
UniV3 LP dynamics between mainnet and arbitrum, and to make people smarter about 
UniV3 liquidity provision in general.

### Project Details

Uniswap V3 liquidity provision is a major source of real yield in DeFi. It is a 
weapon sophisticated players use to make millions while degens get rekt due to 
a lack of analytics/insights performed on complete data at the position level.

At the moment, DeFiLlama provides UniV3 data at the pool level, but not at the 
position level. Revert Finance gathers positions data, but doesn't make the data 
easily accessible. And they only collect data from positions minted with the 
nftmanager contract. Experienced users often mint univ3 positions directly without 
ever interacting with the nftmanager contract, and these data are not collected 
and made public by anyone that we know of.

This project aims to build infrastructure to collect and manage UniV3 positions 
data from mainnet and arbitrum in real time as new positions are opened and old 
ones are removed. We also plan to analyze the data collected using advanced 
statistical methods and machine learning. Finally, we plan to build dashboards 
and data apps for the general public to access our analytics and forecasts.

As a demonstration, we scraped data from Revert Finance's website, trained 
xgboost models to predict ROI and Fee APRs, and built the following dashboards:

- Machine Learning Prediction of ROI and Fee APR of [UniV3 WBTC-WETH positions on Mainnet](https://coindataschool-univ3-roi-prediction-wbtc-weth-main-oufzxi.streamlit.app/) and [WETH-GMX positions on Arbitrum](https://coindataschool-univ3-roi-prediction-weth-gmx-main-ponc95.streamlit.app/).

### Team members

* A team of one data scientist.

## Development Roadmap

### Overview

* **Total Estimated Duration:** 18 months
* **Total Costs:** $300,000

### Milestone 1 -- Data Collection and Management

* **Estimated Duration:** 9 months
* **Costs:** $150,000

| Number | Deliverable |
| ------------- | ------------- |
| 1. | Database in ClickHouse Cloud |
| 2. | ETL workflow in dbt |

### Milestone 2 -- Data Analysis and Visualization

* **Estimated Duration:** 3 months
* **Costs:** $50,000

| Number | Deliverable |
| ------------- | ------------- |
| 1. | Visualize the distributions of ROI, fee APR, and impermanent loss of univ3 positions|
| 2. | Visualize their relationships  |
| 3. | Hypothesis Testing |
| 4. | Ad hoc Statistical Analyses |

### Milestone 3 -- Machine Learning

* **Estimated Duration:** 6 months
* **Costs:** $100,000

| Number | Deliverable |
| ------------- | ------------- |
| 1. | ML models for ROI prediction |
| 2. | ML models for fee APR prediction |
| 3. | Data App that allows user to use these models |
