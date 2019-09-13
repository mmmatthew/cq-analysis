# Merges pure trend with sofi to create signals of desired correlation coefficient value
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt


# creates function to optimize
def load_data(trend_path, noisy_path):
    # Load data
    trend = pd.read_csv(trend_path, sep=';', index_col=0, parse_dates=['datetime'], dayfirst=True)
    noisy = pd.read_csv(noisy_path, sep=';', index_col=0, parse_dates=['datetime'], dayfirst=True)

    # aggregate by second
    trend = trend.resample('S').mean()

    # normalize both so that combination works better
    trend.value = trend.value / trend.value.max()
    noisy.value = noisy.value / noisy.value.max()

    combined = noisy.join(trend, how='inner', lsuffix='_sofi', rsuffix='_trend')

    return combined

def create_merge_function(combined):

    def merge_and_evaluate(sofi_fraction):
        # create or edit merged data
        combined['value'] = combined['value_sofi']*sofi_fraction + combined['value_trend']*(1-sofi_fraction)
        # evaluate spearman correlation coefficient
        correlation = combined.corr(method='spearman')

        return correlation.loc['value_trend', 'value'], combined.copy()

    return merge_and_evaluate


def find_combination(combined, obj_correlation):
    # create function to merge data and estimate correlation
    merge_and_evaluate = create_merge_function(combined)

    # function to minimize
    def f2minimize(x): return np.abs(merge_and_evaluate(x)[0] - obj_correlation)

    # minimization
    result = minimize(f2minimize, np.array([0.9]), method='Nelder-Mead', bounds=[(0, 1)], tol=0.01,
                      # callback=lambda x: print('value: {}'.format(x)),
                      options={'disp': True})
    if result.success:
        print('SUCCESS! {}'.format(result.x))
        return merge_and_evaluate(result.x)[1]
    else:
        print('minimization failed')
        return False

experiment_path = './data/experiment_list.csv'
trend_path_real = './data/all_s3_h_us_maxbotix_normalized.txt'
sofi_path_real = './data/161006A_s3_sofi.txt'
random_path = './data/hybrid/random_gaussian_E20.txt'
template_out_real_path = './data/hybrid_new/sofi_hybrid_c{}.txt'
template_out_random_path = './data/hybrid_new/gaussian_hybrid_c{}.txt'
obj_correlations = [.6, .7, .8, .9]


# Load data
combined = load_data(trend_path_real, sofi_path_real)

# Load experiments
experiments = pd.read_csv(experiment_path, sep=';', index_col=0, parse_dates=['start_datetime', 'end_datetime'], dayfirst=True)

# Loop through experiments 20-24 and get data for each

for objective_correlation in obj_correlations:
    data_all = None
    for i_exp in range(20, 25):
        temp = combined.loc[
                (combined.index <= experiments.loc[i_exp, 'end_datetime']) &
                (combined.index >= experiments.loc[i_exp, 'start_datetime'])]
        print('searching for series for event {} and correlation'.format(i_exp, objective_correlation))
        data = find_combination(temp, objective_correlation)
        if data_all is None:
            data_all = data
        else:
            data_all = data_all.append(data)
    data_all['value'].to_csv(template_out_real_path.format(objective_correlation), sep=';', header=True, date_format='%d/%m/%Y %H:%M:%S')