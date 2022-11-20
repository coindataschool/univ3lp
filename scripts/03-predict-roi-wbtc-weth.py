import pandas as pd
import seaborn as sns
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from xgboost import XGBRegressor 
import os
import joblib

# --- input --- #

chain = 'mainnet'
token0 = '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599' 
token1 = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
init_deposit_cutoff_lwr = 1000 # USD
init_deposit_cutoff_upr = 1e6  # USD
age_cutoff = 0.5 # days
price_lower_cutoff = 5 # lower limit of token0/token1 such as BTCETH
price_upper_cutoff = 60 # upper limit of token0/token1 such as BTCETH

# --- read and filter data --- #

dat = pd.read_pickle('../data/univ3_{}_lps.pkl'.format(chain))

# check min value of liquidity. It should be 50 
# as claimed by revert finance Top Positions page.
dat['underlying_value'].min()

# the API doesn't return positions where people removed 100% 
# liquidity and never added back.
dat.exited.unique()

# only focus on the pair we are interested in
cond1 = (dat.token0 == token0.lower()) & (dat.token1 == token1.lower())
cond2 = (dat.token0 == token1.lower()) & (dat.token1 == token0.lower())
df = dat[cond1 | cond2]
len(df)

# ideally, we'd want to work with a dataset that contains only 
# 1. positions that never experienced partial removals
# 2. positions that never had additional liquidity added
# 3. positions that ran its course and had 100% liquidity 
#    removed and no new liquidity added.
# We don't have 3, but can get a dataset of 1 and 2.

# only look at positions that hasn't even once removed liquidity
cond3 = (df.total_withdrawn1 == 0) & (df.total_withdrawn0 == 0)
# autocompounding is an indirect way of adding liquidity, so we ignore them
cond4 = ~df.autocompounding
df = df[cond3 & cond4]
len(df)

# positions without additional liquidity added after initial deposits satisfy 
# the equality below
cond5 = (abs(df.underlying_value - (df.deposits_value + df.il)) < 0.1)
# df.loc[~cond5, ['underlying_value', 'deposits_value', 'il']].head()
df = df[cond5]
len(df)

# only look at positions with at least $X initial deposits
cond6 = (df.deposits_value >= init_deposit_cutoff_lwr) & \
        (df.deposits_value < init_deposit_cutoff_upr)
# only look at positions with at least X days
cond7 = df.age >= age_cutoff
df = df[cond6 & cond7]
len(df)

# drop positions with ridiculous price limits that cover the full range
cond8 = (df.price_lower >= price_lower_cutoff) & \
        (df.price_upper <= price_upper_cutoff)
df = df[cond8]
len(df)

# only focus on these columns
cols = ['fee_tier', 'age', 'in_range', 'deposits_value', 'il', 
        'roi', 'apr', 'fee_apr', # 'pool_apr', # pool_apr is apr_excluding_gas
        'price_upper', 'price_lower']
df = df[cols]

# change data types
df['fee_tier'] = (df.fee_tier / 1e4).astype(str) + '%'
df['fee_tier'] = df['fee_tier'].astype('category')
df['in_range'] = df.in_range.astype(int)
df['price_rng_width'] = df.price_upper - df.price_lower
for pct_var in ['roi', 'apr', 'fee_apr']:
    df[pct_var] = df[pct_var] / 100
# df.select_dtypes(['category'])

# drop 1%-fee-tier positions since there are only a few of them
df.fee_tier.value_counts()
df = df[df.fee_tier != '1.0%']
df['fee_tier'] = df.fee_tier.cat.remove_unused_categories()
df.fee_tier.value_counts()
len(df)

# --- explore data --- #

yvar = 'roi'

# # univariate distributions
# sns.displot(df, x=yvar, hue='fee_tier')
# sns.displot(df, x='age', hue='fee_tier')
# sns.displot(df, x='deposits_value', log_scale=True, hue='fee_tier')
# sns.displot(df, x='price_rng_width', hue='fee_tier')
# sns.displot(df, x='price_lower', hue='fee_tier')
# sns.displot(df, x='price_upper', hue='fee_tier')

# # bivariate relationships
# sns.relplot(df, x='age', y=yvar, hue='fee_tier')
# sns.relplot(df, x='price_rng_width', y=yvar, hue='fee_tier')
# g = sns.relplot(df, x='deposits_value', y=yvar, hue='fee_tier')
# g.set(xscale='log')

print("Ranges of Sample Data Variables:")
print("- Age ranges from {} to {} days".format(
    df.age.min().round(1), df.age.max().round(1)))
print("- Deposit ranges from {} to {} USD".format(
    df.deposits_value.min().round(1), df.deposits_value.max().round(1)))
print("- Price lower limit ranges from {} to {}".format(
    df.price_lower.min().round(1), df.price_lower.max().round(1)))
print("- Price upper limit ranges from {} to {}".format(
    df.price_upper.min().round(1), 
    df.price_upper.max().round(1)), end='\n\n')

# --- ML --- #

xvars_num = ['age', 'price_lower', 'price_upper'] # 'price_rng_width' 
xvars_cat = ['fee_tier']

# split data into training (80%) and test (20%) sets
# we'll train model on the training set with cv and 
# save the test set for final eval of model performance.
Xtrain, Xtest, ytrain, ytest = train_test_split(
    df[xvars_num + xvars_cat], df[yvar], 
    test_size=0.2, random_state=42)

# define column transformers to
# 1. standardize the numeric features so that they are on similar scale, and
# 2. one-hot encode the categorical features
transformer_num = Pipeline(steps=[('scaler', StandardScaler())])
transformer_cat = OneHotEncoder()
preprocessor = ColumnTransformer(
    transformers=[
        ('num', transformer_num, xvars_num),
        ('cat', transformer_cat, xvars_cat)
    ]
)
# Xtrain_scaled = preprocessor.fit_transform(Xtrain)
# Xtrain_scaled[:4]

# specify xgboost regressor
xgb_reg_model = XGBRegressor(objective="reg:squarederror", random_state=123)

# chain preprocessor and xgboost regressor into a full prediction pipeline
pipeline = Pipeline(
    steps=[('preprocessor', preprocessor), 
           ('regressor', xgb_reg_model)]
    )

# set up grid search with 5-fold cross-validation
param_grid = {
    'regressor__learning_rate': [0.005, 0.01, 0.02, 0.1],
    # # try tuning the other params: 
    #  "regressor__max_depth": [4, 6, 8, 10, 12],
    #  "regressor__min_child_weight": [ 1, 3, 5, 7],
    #  "regressor__gamma":[ 0.0, 0.1],
    #  "regressor__colsample_bytree":[0.3, 0.4]
}
grid = GridSearchCV(
    pipeline, 
    param_grid,    
    scoring = 'neg_mean_absolute_error',
    refit   = True,
    cv      = 5
)

# run grid search
grid.fit(Xtrain, ytrain)
print('Training sample size:', len(Xtrain))
print("Best params:")
print(grid.best_params_)
print("Internal CV score: {:.3f}".format(grid.best_score_))
print("Test score of the best model from grid search: {:.3f}".format(grid.score(Xtest, ytest)))

# predict 
df_pred = ytest.to_frame()
df_pred['xgb_pred'] = grid.predict(Xtest)
df_pred.head()

# save
os.makedirs('../output', exist_ok=True)
joblib.dump(grid, '../output/xgb_model_{}.joblib'.format(yvar))
pd.to_pickle(df_pred, '../output/xgb_pred_{}.pkl'.format(yvar))