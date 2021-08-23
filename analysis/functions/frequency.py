import csv
import datetime
import os
import time

import analysis.utils.constants as constants
import analysis.utils.helpers as helpers


def main(result_dict, df, chat_members, args):
    if not args.graph_time_interval:
        raise Exception('Must give time interval length for graph')

    message_freqs = {}
    if args.graph_individual:
        members = []
        for member_name in chat_members:
            helpers.initialize_member(member_name, result_dict)
            if helpers.get_total_messages(df, member_name) > 0:
                members.append(member_name)
        for member in members:
            message_freqs[member] = []
    else:
        message_freqs['total messages'] = []

    if args.graph_time_interval == 'day':
        df['time_period'] = df['time'].apply(helpers.get_day)
    elif args.graph_time_interval == 'week':
        df['time_period'] = df['time'].apply(helpers.get_week)
    elif args.graph_time_interval == 'month':
        df['time_period'] = df['time'].apply(helpers.get_month)
    elif args.graph_time_interval == 'year':
        df['time_period'] = df['time'].apply(helpers.get_year)

    day_fmt = '%m/%d/%y'
    begin_date = datetime.datetime.strptime(df['time_period'].iloc[0], day_fmt)
    end_date = datetime.datetime.strptime(df['time_period'].iloc[-1], day_fmt)
    time_periods = helpers.get_time_periods(begin_date, end_date, args.graph_time_interval)
    for time_period in time_periods:
        if args.graph_individual:
            for member_name in members:
                message_freqs[member_name].append(len(
                    df[(df['time_period'] == time_period) & (df['sender'] == member_name)]
                ))
        else:
            message_freqs['total messages'].append(len(
                df[df['time_period'] == time_period]
            ))

    result_dict['graphData'] = {}

    if args.day or args.week:
        result_dict['graphData']['labels'] = time_periods
    elif args.month:
        result_dict['graphData']['labels'] = [
            f'{time_period.split("/")[0]}/{time_period.split("/")[2]}'
            for time_period in time_periods
        ]
    elif args.year:
        result_dict['graphData']['labels'] = [
            f'20{time_period.split("/")[2]}'
            for time_period in time_periods
        ]

    result_dict['graphData']['datasets'] = [
        {
            'label': name,
            'data': message_freqs[name],
            'fill': False,
            'borderColor': constants.GRAPH_COLORS[i % len(message_freqs)]
        }
        for i, name in enumerate(message_freqs)
    ]
