from datetime import datetime
import pandas as pd


def date_transform(string, informat, outformat):
    return datetime.strftime(datetime.strptime(string, informat), outformat)


def get_events(identifiers, metadata_path, initial_condition_path):
    events_df = pd.read_csv(metadata_path, sep=';')
    date_format_in = '%d.%m.%y %H:%M'
    date_format_out = '%Y/%m/%d %H:%M:%S'

    initial_conditions = pd.read_csv(initial_condition_path, index_col=0)

    # use rules to set certain initial conditions
    initial_conditions['id_1'] = initial_conditions.id_m2 + 0.21
    initial_conditions['id_v9'] = initial_conditions.id_s5
    initial_conditions['id_4'] = initial_conditions.id_s5 + 0.68
    initial_conditions['id_9'] = initial_conditions.id_s5 + 0.68
    initial_conditions['id_v8'] = initial_conditions.id_s5
    initial_conditions['id_v7'] = initial_conditions.id_s5
    initial_conditions['id_v4'] = initial_conditions.id_s5
    initial_conditions['id_m3'] = initial_conditions.id_s5 + 0.5

    # transform to dict
    initial_conditions = initial_conditions.to_dict('index')

    events_formatted = {}

    for idx in identifiers:
        event = {'name': '{}'.format(idx),
                 'start_dt': date_transform(events_df[events_df['id'] == idx]['start_datetime'].item(),
                                            date_format_in,
                                            date_format_out),
                 'end_dt': date_transform(events_df[events_df['id'] == idx]['end_datetime'].item(), date_format_in,
                                          date_format_out),
                 'initial_conditions': initial_conditions[idx]
                 }

        events_formatted[idx] = event

    return events_formatted
