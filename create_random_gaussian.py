# Create a timeseries of random data between two dates
from datetime import datetime
import pandas as pd
import numpy as np

outfile = './data/hybrid/random_gaussian_E20.txt'

# Start and end date
date_start = datetime(2016, 10, 6, 14)
date_end = datetime(2016, 10, 6, 18)

# create date range
time = pd.date_range(date_start, date_end, freq='S', name='datetime')
random_data = np.random.randn(len(time))

data = pd.DataFrame(data={'value': random_data}, index=time)
# Save data
data['value'].to_csv(outfile, sep=';', header=True, date_format='%d/%m/%Y %H:%M:%S')