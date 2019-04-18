from swmm_calibration.classes import experiment_runner
import itertools
import os
import sys
import gc
import helpers as h
import settings

overwrite = False
event_identifiers = [20, 21, 22, 23, 24]
if len(sys.argv) > 0:
    calibrate_events = [int(sys.argv[1])]
else:
    calibrate_events = event_identifiers
print('calibrating with {}'.format(calibrate_events))

# event_identifiers = [20, 21]
# locations_available = ['c3']
locations_available = ['s3', 's5', 's6']
data_types = ['trend', 'sensor']
event_metadata = 'data/experiment_list.csv'
ic_path = 'data/initial_conditions.csv'

workdir = 'Q:/Messdaten/floodVisionData/core_2018_cq/_temp/with_iterations/'
# define log file
log_file = os.path.join(workdir, 'results.csv')
if os.path.isfile(log_file) and overwrite:
    print('removing last results')
    os.remove(log_file)

events = h.get_events(identifiers=event_identifiers, metadata_path=event_metadata, initial_condition_path=ic_path)

for event_number in calibrate_events:
    for source_count in [4, 3, 2, 1]:
        for locations in list(itertools.combinations(locations_available, source_count)):
            for types in itertools.product(data_types, repeat=source_count):
                for repetition in range(10):
                    obses = []
                    for location, type in zip(locations, types):
                        obses.append(location + '_' + type)
                    print('#  Calibrating with Experiment {} using {}: iteration {}'
                          .format(event_number, '-'.join(obses), repetition))

                    # define calibration event
                    calibration_event = events[event_number]
                    # find other events
                    validation_event_numbers = [i for i in event_identifiers if i != event_number]
                    validation_events = [events[i] for i in validation_event_numbers]

                    # define directory
                    exp_dir = os.path.join(workdir, '-'.join(obses), str(event_number), str(repetition))

                    # check if processing already performed for directory
                    if os.path.isfile(os.path.join(exp_dir, 'calibration_chain.png')) and not overwrite:
                        print('Processing already performed')
                        continue

                    # create new settingss
                    s = settings.Settings

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
                            'count_trend': types.count('trend'),
                            'repetition': repetition
                        }, evaluation_count=1
                    )
                    runner.run(repetitions=2000, kstop=8, ngs=3, pcento=0.5)
                    # delete settings and runner
                    del s
                    del runner
                    # collect garbage
                    gc.collect()
