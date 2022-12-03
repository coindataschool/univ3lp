# Bring Uniswap V3 LP Positions Data and Analytics to the General Public

* **Project Name:** Collecting, Analysis, and Modeling of Uniswap V3 LP Positions Data
* **Team Name:** (TBD)

## Project Overview

We would like to gather, visualize, analyze, and model mainnet and L2 Uniswap V3 
LP positions data to uncover patterns of LP behavior/distribution so that the 
general public becomes smarter when it comes to liquidity provision. 

### Overview

Uniswap V3 liquidity provision is one major source of real yield in DeFi. It is 
a weapon sophisticated players use to make millions while most degens get rekt 
due to a lack of understanding of how it works and how impermanent loss manifests 
over time.

This project aims to build infrastructure that gathers all of UniV3 positions 
data from mainnet and L2s in real time as new positions are opened and old ones 
are removed. And we plan to build an ETL workflow system to solve-once and deploy 
forever any data transformations, and an enterprise-grade MLOps platform built 
on DataBricks (or Open Source equivalent) for fast model development and 
deployment. Finally, we will build dashboards and websites for the general 
public to access our data and analytics.

### Project Details

DeFiLlama alreadys provides UniV3 data at the pool level, but not at individual 
position level. Revert Finance gathers positions data, but don't make them easily 
accessible. And they only collect data from positions created with the nftmanager 
contract. Experienced users often mint univ3 positions directly without ever 
interacting with the nftmanager contract, and these data are not collected by 
Revert Finance or anyone that we know of. Finally, to our best knowledge, no team
has studied the LP behaviors using advanced statistical analysis or tried to 
predict the ROI and fee APRs using machine learning. Those are the things we 
want to accomplish with the help of this grant.

To demonstrate, we scraped data from Revert Finance's website, trained xgboost 
models to predict ROI and Fee APRs, and built the following dashboards:

- Machine Learning Prediction of ROI and Fee APR of [UniV3 WBTC-WETH positions on Mainnet](https://coindataschool-univ3-roi-prediction-wbtc-weth-main-oufzxi.streamlit.app/) and [WETH-GMX positions on Arbitrum](https://coindataschool-univ3-roi-prediction-weth-gmx-main-ponc95.streamlit.app/).

### Team members

* A team of (how many) data engineer and (how many) data scientist who has built (what)

## Development Roadmap

### Overview

* **Total Estimated Duration:** 12 months
* **Total Costs:** $750,000

### Milestone 1 -- Data Gathering and Management

* **Estimated Duration:** 5 months
* **Costs:** (how much?)

| Number | Deliverable | Specification |
| ------------- | ------------- | ------------- |
| 0a. | License | xxx |
| 1. | xxxx | xxxx |
| 2. | xxxx | xxxx | 
| 3. | xxxx | xxxx｜

### Milestone 2 -- Data Analysis and Visualization

* **Estimated Duration:** 2 months
* **Costs:** (how much?)

| Number | Deliverable | Specification |
| ------------- | ------------- | ------------- |
| 1. | xxxx | xxxx |

### Milestone 3 -- Machine Learning, Predicting ROIs and Fee APRs

* **Estimated Duration:** 5 months
* **Costs:** (how much?)

| Number | Deliverable | Specification |
| ------------- | ------------- | ------------- |
| 1. | xxxx | xxxx |