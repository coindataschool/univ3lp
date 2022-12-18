from statsmodels.tsa.stattools import coint, adfuller
from statsmodels.stats.stattools import jarque_bera
import pandas as pd

def check_stationarity(x: pd.Series, sig_level=0.01):
    """
    Check if a time series is stationary.
    H0: unit root exists (non-stationary). 
    So if the p-value is less than `sig_level`, we'd reject H0 and conclude the 
    series is stationary.

    Parameters
    ----------
    x : Series
    sig_level : float
        Significance level below which we'd conclude statistical significance.
    """

    pval = adfuller(x)[1]  # the augmented Dickey– Fuller test
    msg = 'p-value = ' + str(round(pval, 4)) + ', and the time series ' 
    if x.name != None:
        msg += x.name
    if pval < sig_level:
        print(msg + ' is likely stationary.')
        return True
    else:
        print(msg + ' is likely non-stationary.')
        return False

def check_normality(x: pd.Series, sig_level=0.01):
    """
    Check if a time series is normally distributed.
    H0: not normal.
    So if the p-value is less than `sig_level`, we'd reject H0 and conclude the 
    series is normally distributed.

    Parameters
    ----------
    x : Series
    sig_level : float
        Significance level below which we'd conclude statistical significance.
    """

    pval = jarque_bera(x)[1]
    msg = 'p-value = ' + str(round(pval, 4)) + ', and the time series ' 
    if x.name != None:
        msg += x.name
    if pval < sig_level:
        print(msg + ' is likely normally distributed.')
        return True
    else:
        print(msg + ' is likely not normally distributed.')
        return False

def check_coint(x1: pd.Series, x2: pd.Series, sig_level=0.01):
    """
    Check if two time series are cointegrated.
    H0: not cointegrated.
    So if the p-value is less than `sig_level`, we'd reject H0 and conclude the 
    two series are cointegrated.

    Parameters
    ----------
    x1 : Series
    x2 : Series
    sig_level : float
        Significance level below which we'd conclude statistical significance.
    """

    pval = coint(x1, x2)[1]
    msg = 'p-value = ' + str(round(pval, 4)) + ', and the two time series ' 
    if pval < sig_level:
        print(msg + 'are likely cointegrated.')
        return True
    else:
        print(msg + 'are likely not cointegrated.')
        return False

# # test
# T = 100
# 
# A = pd.Series(index=range(T))
# A.name = 'A'
#
# B = pd.Series(index=range(T))
# B.name = 'B'
#
# for t in range(T):
#       A[t] = np.random.normal(0, 1)
#       B[t] = np.random.normal(np.sin(t), 1)
#
# check_stationarity(A)
# check_normality(A, 0.05)
# check_coint(A, B)