# import tsdeg
from swmm_calibration.classes import experiment_runner
import itertools
import os
import helpers as h
import settings

event_identifiers = [20, 21, 22, 23, 24]
locations_available = ['s3', 's5', 's6']
data_types = ['trend', 'sensor']
event_metadata = 'data/experiment_list.csv'

workdir = 'Q:/Messdaten/floodVisionData/core_2018_cq/_temp'
# define log file
log_file = os.path.join(workdir, 'results.csv')

events = h.get_events(identifiers=event_identifiers, metadata_path=event_metadata)

for event_number in event_identifiers:
    for source_count in [1, 2, 3]:
        for locations in list(itertools.combinations(locations_available, source_count)):
            for types in itertools.product(data_types, repeat=source_count):
                obses = []
                for location, type in zip(locations, types):
                    obses.append(location + '_' + type)
                print('Calibrating with Experiment {} using {}'.format(event_number, '-'.join(obses)))

                # define calibration event
                calibration_event = events[event_number]
                # find other events
                validation_event_numbers = [i for i in event_identifiers if i != event_number]
                validation_events = [events[i] for i in validation_event_numbers]

                # create new settings
                s = settings.Settings

                # adapt settings
                s.calibration_event = calibration_event
                s.validation_events = validation_events

                # choose observations to use for calibration
                s.obs_config_calibration = obses

                # define directory
                exp_dir = os.path.join(workdir, '-'.join(obses), str(event_number))

                # create experiment runner
                runner = experiment_runner.ExperimentRunner(data_directory=exp_dir, output_file=log_file,
                                                            settings=s, experiment_metadata={
                        'event': event_number,
                        'observations': '-'.join(obses),
                        'source_count': source_count,
                        'count_sensor': types.count('sensor'),
                        'count_trend': types.count('trend')
                    })
                runner.run(repetitions=1000, kstop=5, ngs=5, pcento=0.5)
                # delete settings and runner
                del s
                del runner
