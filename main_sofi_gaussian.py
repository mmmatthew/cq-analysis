from swmm_calibration.classes import experiment_runner
import itertools
import os
import sys
import gc
import helpers as h
import settings

overwrite = False
event_identifiers = [20, 21, 22, 23, 24]

# Find out which events to calibrate
if len(sys.argv) > 1:
    calibrate_events = sys.argv[1:]
else:
    calibrate_events = event_identifiers
print('calibrating with {}'.format(calibrate_events))

locations_available = ['s3', 's5', 's6']
data_types = ['trend', 'sensor']
event_metadata = 'data/experiment_list.csv'
ic_path = 'data/initial_conditions.csv'

workdir = 'Q:/Messdaten/floodVisionData/core_2018_cq/4_experiments/CliBU008/simple_model/190913_update_hybrid/'
# define log file
log_file = os.path.join(workdir, 'results gaussian {}.csv'.format(' '.join(map(str, calibrate_events))))
if os.path.isfile(log_file) and overwrite:
    print('removing last results')
    os.remove(log_file)

events = h.get_events(identifiers=event_identifiers, metadata_path=event_metadata, initial_condition_path=ic_path)

for repetition in range(10):
    for quality in [.6, .7, .8, .9]:

        sofi_obs_name = 's3_gaussiantrend_{}'.format(quality)

        for obses, types in zip([[sofi_obs_name, 's6_trend'], [sofi_obs_name]], [['gaussiantrend', 'trend'], ['gaussiantrend']]):
            for event_number in [23, 24]:
                source_count = len(obses)

                # define calibration event
                calibration_event = events[event_number]
                # find other events
                validation_event_numbers = [i for i in event_identifiers if i != event_number]
                validation_events = [events[i] for i in validation_event_numbers]

                print('#  Calibrating with Experiment {} using {}: iteration {}'
                      .format(event_number, '-'.join(obses), repetition))
                # define directory
                exp_dir = os.path.join(workdir, '-'.join(obses), str(event_number), str(repetition))

                # check if processing already performed for directory
                if os.path.isfile(os.path.join(exp_dir, 'parameter_sampling_distributions.png')) and not overwrite:
                    print('Processing already performed')
                    continue

                # create new settings
                s = settings.Settings

                # create observation for specific sofi trend quality
                s.obs_available[sofi_obs_name] = {
                    "data_file": './data/hybrid_new/gaussian_hybrid_c{}.txt'.format(quality),
                    "location": 's3',
                    "data_type": 'trend',
                    "scale_factor": 1,
                    "swmm_node": ['node', 's3', 'Depth_above_invert'],
                    "calibration": {
                        "obj_fun": 'spearman_simple_zero',
                        "weight": -0.5,
                "zero_threshold_obs": 0.02,  # for spearman zero obj_fun, we define a
                "zero_threshold_sim": 0.02
                    }
                }

                # adapt settings
                s.calibration_event = calibration_event
                s.validation_events = validation_events

                # choose observations to use for calibration and validation
                s.obs_config_calibration = obses

                # create experiment runner
                runner = experiment_runner.ExperimentRunner(
                    data_directory=exp_dir, output_file=log_file, settings=s, experiment_metadata={
                        'event_cal': event_number,
                        'observations': '-'.join(obses),
                        'source_count': source_count,
                        'count_sensor': types.count('sensor'),
                        'count_trend': types.count('trend') + types.count('gaussiantrend'),
                        'repetition': repetition
                    }, evaluation_count=1, experiment_name='-'.join(obses)
                )
                runner.run(repetitions=2000, kstop=8, ngs=7, pcento=0.5)
                # delete settings and runner
                del s
                del runner
                # collect garbage
                gc.collect()
