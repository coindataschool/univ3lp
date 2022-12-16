# TODO

## Collect Data

Build infrastructure/workflow to collect and manage UniV3 positions data in real time.

DeFiLlama provides UniV3 data at the pool level but not at individual position 
level. Revert Finance gathers positions data, but don't make them easily 
accessible. And they only collect data from positions created with the nftmanager 
contract, leaving out positions minted directly without ever interacting with the 
nftmanager contract.

Must: solve-once and deploy forever any data transformations.

## Visualize Data

TBD

## Machine Learning

Build an enterprise-grade MLOps platform on DataBricks (or alternative) for fast 
model development.