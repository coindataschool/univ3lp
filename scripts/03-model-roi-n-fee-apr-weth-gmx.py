import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from xgboost import XGBRegressor 
import os
import joblib

# --- input --- #

chain = 'arbitrum'
token0 = dict(
    symbol = 'weth', addr = '0x82aF49447D8a07e3bd95BD0d56f35241523fBab1')
token1 = dict(
    symbol = 'gmx', addr = '0xfc5A1A6EB076a2C7aD06eD22C90d7E710E35ad0a')
init_deposit_cutoff_lwr = 50 # USD
init_deposit_cutoff_upr = 1e6  # USD
age_cutoff = 3/24 # days
price_lower_cutoff = 4 # lower limit of token0/token1 such as ETHGMX
price_upper_cutoff = 400 # upper limit of token0/token1 such as ETHGMX


# --- create subdir and base name for saving files --- #

os.makedirs('../png', exist_ok=True)
os.makedirs('../output', exist_ok=True)
save_fname_base = '{}-{}-{}-'.format(chain, token0['symbol'], token1['symbol'])

# --- read and filter data --- #

dat = pd.read_pickle('../data/univ3_{}_lps.pkl'.format(chain))

# check min value of liquidity. It should be 50 
# as claimed by revert finance Top Positions page.
dat['underlying_value'].min()

# the API doesn't return positions where people removed 100% 
# liquidity and never added back.
dat.exited.unique()

# only focus on the pair we are interested in
cond1 = (dat.token0 == token0['addr'].lower()) & (dat.token1 == token1['addr'].lower())
cond2 = (dat.token0 == token1['addr'].lower()) & (dat.token1 == token0['addr'].lower())
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

# drop positions with 0 fee apr
df = df[df.fee_apr > 0]
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
df = df[df.fee_tier != '0.05%']
df['fee_tier'] = df.fee_tier.cat.remove_unused_categories()
df.fee_tier.value_counts()
len(df)

# --- explore data --- #

print('Making plots and save them to disk...')

# univariate distributions without log transformation
cols = ['roi', 'price_lower']
for var in cols:
    sns.displot(df, x=var, hue='fee_tier')
    plt.savefig('../png/'+save_fname_base+'{}.png'.format(var), dpi=300)
# univariate distributions with log transformation
log_cols = ['fee_apr', 'age', 'price_rng_width', 'price_upper']
for var in log_cols:
    sns.displot(df, x=var, hue='fee_tier', log_scale=True)
    plt.savefig('../png/'+save_fname_base+'{}.png'.format(var), dpi=300)

# bivariate relationships
for yvar in ['roi', 'fee_apr']:
    for xvar in ['age', 'price_rng_width', 'price_lower', 'price_upper']:
        g = sns.relplot(df, x=xvar, y=yvar, hue='fee_tier')
        if xvar != 'price_lower':
            g.set(xscale='log')
        if yvar == 'fee_apr': 
            g.set(yscale='log') 
        fnm = '../png/'+save_fname_base+'{}-vs-{}.png'.format(yvar, xvar)
        plt.savefig(fnm, dpi=300)

# take the log1p transform of fee_apr for ML since it's right skewed
df['log1p_fee_apr'] = np.log1p(df['fee_apr'])

# print ranges of key variables
print("Ranges of Sample Data Variables:")
print("- Age ranges from {:.3f} to {:.3f} days".format(
    df.age.min(), df.age.max()))
print("- Deposit ranges from {:.1f} to {:.1f} USD".format(
    df.deposits_value.min(), df.deposits_value.max()))
print("- Price lower limit ranges from {:.1f} to {:.1f}".format(
    df.price_lower.min(), df.price_lower.max()))
print("- Price upper limit ranges from {:.1f} to {:.1f}".format(
    df.price_upper.min(), df.price_upper.max()))
print("- ROI ranges from {:.2%} to {:.2%}".format(
    df.roi.min(), df.roi.max()))
print("- Fee APR ranges from {:.2%} to {:.2%}".format(
    df.fee_apr.min(), df.fee_apr.max()), end='\n\n')

# --- ML --- #

# group features based on the kind of transformations we'll do to them
xvars_log = ['age', 'price_rng_width', 'price_upper']
xvars_scale = ['price_lower'] 
xvars_cat = ['fee_tier']

# define column transformers to
# 1. log-transform the right-skewed features
# 2. standardize the other numeric features 
# 3. one-hot encode the categorical features
preprocessor = ColumnTransformer(
    transformers=[
        ('log', FunctionTransformer(np.log1p, validate=False), xvars_log),
        ('scale', StandardScaler(), xvars_scale),
        ('cat', OneHotEncoder(), xvars_cat)
    ],
    remainder='passthrough'
)

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
    #  "regressor__gamma":[0.0, 0.1],
    #  "regressor__colsample_bytree":[0.3, 0.4]
}
grid = GridSearchCV(
    pipeline, 
    param_grid,    
    scoring = 'neg_mean_absolute_error',
    refit   = True,
    cv      = 5
)

# let's build two models, one for ROI prediction and the other for fee APR 
# prediction. Because we've seen in the plots that fee apr is right skewed, 
# we'll train a model to predict log1p(fee apr) instead of fee apr directly.
for yvar in ['roi', 'log1p_fee_apr']:
    print('Train a xgboost model to predict {}...'.format(yvar))
    
    # split data into training (80%) and test (20%) sets
    # we'll train model on the training set with cv and 
    # save the test set for final eval of model performance.
    Xtrain, Xtest, ytrain, ytest = train_test_split(
        df[xvars_log + xvars_scale + xvars_cat], df[yvar], 
        test_size=0.2, random_state=42)
    print('Training sample size:', len(Xtrain))
    print('Test sample size:', len(Xtest))
        
    # run grid search
    grid.fit(Xtrain, ytrain)
    print("Best params:")
    print(grid.best_params_)
    print("Internal CV score: {:.3f}".format(grid.best_score_))
    print("Test score of the best model from grid search: {:.3f}"\
        .format(grid.score(Xtest, ytest)), end='\n\n')

    # predict 
    df_pred = ytest.to_frame()
    df_pred['xgb_pred'] = grid.predict(Xtest)
    if yvar == 'log1p_fee_apr':
        df_pred = np.exp(df_pred) - 1
        df_pred = df_pred.rename(columns={yvar:'fee_apr'})

    # save
    model_fname = save_fname_base+'xgbmod-{}.joblib'.format(yvar)
    joblib.dump(grid, '../output/' + model_fname)
    pred_fname = save_fname_base+'xgbpred-{}.pkl'.format(yvar.replace('log1p_',''))
    pd.to_pickle(df_pred, '../output/' + pred_fname)