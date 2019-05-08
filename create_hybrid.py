# Merges pure trend with sofi to create signals of desired correlation coefficient value
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt


# creates function to optimize
def create_merge_function(trend_path, sofi_path):
    # Load data
    trend = pd.read_csv(trend_path, sep=';', index_col=0, parse_dates=['datetime'], dayfirst=True)
    sofi = pd.read_csv(sofi_path, sep=';', index_col=0, parse_dates=['datetime'], dayfirst=True)

    # aggregate by second
    trend = trend.resample('S').mean()

    # normalize both so that combination works better
    trend.value = trend.value/trend.value.max()
    sofi.value = sofi.value/sofi.value.max()
    combined = sofi.join(trend, how='inner', lsuffix='_sofi', rsuffix='_trend')

    def merge_and_evaluate(sofi_fraction):
        # create or edit merged data
        combined['value'] = combined['value_sofi']*sofi_fraction + combined['value_trend']*(1-sofi_fraction)
        # evaluate spearman correlation coefficient
        correlation = combined.corr(method='spearman')

        return correlation.loc['value_trend', 'value'], combined.copy()

    return merge_and_evaluate


def find_combination(trend_path, sofi_path, obj_correlation):
    # create function to merge data and estimate correlation
    merge_and_evaluate = create_merge_function(trend_path, sofi_path)

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


trend_path_real = './data/all_s3_h_us_maxbotix_normalized.txt'
sofi_path_real = './data/161006A_s3_sofi.txt'
template_out_path = './data/hybrid/sofi_hybrid_{}.txt'
obj_correlations = [.6]


for objective_correlation in obj_correlations:
    data = find_combination(trend_path_real, sofi_path_real, objective_correlation)
    # fig = data.plot(title='{}% correlation'.format(objective_correlation))
    # plt.show()
    # save data
    data['value'].to_csv(template_out_path.format(objective_correlation), sep=';', header=True, date_format='%d/%m/%Y %H:%M:%S')
