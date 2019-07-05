from datetime import datetime
import pandas as pd


def date_transform(string, informat, outformat):
    return datetime.strftime(datetime.strptime(string, informat), outformat)


def get_events(identifiers, metadata_path, initial_condition_path):
    events_df = pd.read_csv(metadata_path, sep=';')
    date_format_in = '%d.%m.%y %H:%M'
    date_format_out = '%Y/%m/%d %H:%M:%S'

    initial_conditions = pd.read_csv(initial_condition_path, index_col=0).to_dict('index')

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
