from swmm_calibration.classes import experiment_runner
import itertools
import os
import gc
import helpers as h
import settings

overwrite: bool = True

# event_identifiers = [20, 21]
event_identifiers = [20, 21, 22, 23, 24]
# locations_available = ['c3']
locations_available = ['s3', 's5', 's6']
data_types = ['trend', 'sensor']
event_metadata = 'data/experiment_list.csv'
ic_path = 'data/initial_conditions.csv'

workdir = 'Q:/Messdaten/floodVisionData/core_2018_cq/_temp/190403_b'
# define log file
log_file = os.path.join(workdir, 'results_uncalibrated.csv')
if os.path.isfile(log_file) and overwrite:
    os.remove(log_file)

events = h.get_events(identifiers=event_identifiers, metadata_path=event_metadata, initial_condition_path=ic_path)

for event_number in event_identifiers:
    print('#  Running uncalibrated Experiment {}'.format(event_number))

    # define calibration event
    calibration_event = events[event_number]

    # define directory
    exp_dir = os.path.join(workdir, '_uncalibrated', str(event_number))

    # check if processing already performed for directory
    if os.path.isfile(os.path.join(exp_dir, 'calibration_chain.png')) and not overwrite:
        print('Processing already performed')
        continue

    # create new settings
    s = settings.Settings

    # adapt settings
    s.calibration_event = calibration_event

    # evaluate performance with all possible sensors
    s.obs_config_calibration = [
            's3_sensor',
            's5_sensor',
            's6_sensor'
        ]
    s.obs_config_validation = [
            's3_sensor',
            's5_sensor',
            's6_sensor'
        ]

    # create experiment runner
    runner = experiment_runner.ExperimentRunner(
        data_directory=exp_dir, output_file=log_file, settings=s, experiment_metadata={
            'event_cal': event_number,
            'observations': 'uncalibrated',
            'source_count': 0,
            'count_sensor': 0,
            'count_trend': 0
        })
    runner.evaluate_uncalibrated(count=100)
    # delete settings and runner
    del s
    del runner
    # collect garbage
    gc.collect()
