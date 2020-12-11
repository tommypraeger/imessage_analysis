import csv
import datetime
import os
import time

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from analysis.utils.initialize_result_dict import initialize_result_dict
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers


def main(result_dict, df, chat_members, args):
    if not (args.day or args.week or args.month or args.year):
        raise Exception('Must give time period length for graph')

    message_freqs = {
        'Total Messages': []
    }
    if args.graph_individual:
        members = []
        for member_name in chat_members:
            total_messages, _ = initialize_result_dict(
                member_name, df, result_dict)
            if total_messages > 0:
                members.append(member_name)
        for member in members:
            message_freqs[member] = []
    if args.day:
        df['time_period'] = df['time'].apply(helpers.get_day)
        time_period_name = 'day'
    elif args.week:
        df['time_period'] = df['time'].apply(helpers.get_week)
        time_period_name = 'week'
    elif args.month:
        df['time_period'] = df['time'].apply(helpers.get_month)
        time_period_name = 'month'
    elif args.year:
        df['time_period'] = df['time'].apply(helpers.get_year)
        time_period_name = 'year'

    day_fmt = '%m/%d/%y'
    begin_date = datetime.datetime.strptime(df['time_period'].iloc[0], day_fmt)
    end_date = datetime.datetime.strptime(df['time_period'].iloc[-1], day_fmt)
    time_periods = helpers.get_time_periods(begin_date, end_date, time_period_name)
    for time_period in time_periods:
        message_freqs['Total Messages'].append(len(
            df[df['time_period'] == time_period]
        ))
        if args.graph_individual:
            for member_name in members:
                message_freqs[member_name].append(len(
                    df[(df['time_period'] == time_period) & (df['sender'] == member_name)]
                ))

    fig, ax = plt.subplots()

    x = [datetime.datetime.strptime(d, day_fmt).date() for d in time_periods]

    for key in message_freqs:
        ax.plot(x, message_freqs[key], label=key)

    if args.day or args.week:
        ax.xaxis.set_major_formatter(mdates.DateFormatter(day_fmt))
        ax.xaxis.set_major_locator(mdates.DayLocator())
    elif args.month:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
    elif args.year:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_minor_locator(mdates.MonthLocator())

    ax.xaxis.set_major_locator(plt.MaxNLocator(20))
    fig.autofmt_xdate()

    ax.set_title(f'{args.name}, by {time_period_name}')
    ax.set_xlabel('Date')
    ax.set_ylabel('# of Messages')
    ax.legend()
    time_stamp = int(time.time())
    os.system('rm ui/public/graph_*.png')
    image_path = f'ui/public/graph_{time_stamp}.png'
    plt.savefig(image_path, bbox_inches='tight')
    result_dict['imagePath'] = image_path.split('/')[-1]

    message_freqs['Date'] = []
    for time_period in time_periods:
        message_freqs['Date'].append(time_period)
    csv_file = 'message_frequencies.csv'
    with open(csv_file, 'w') as f:
        keys = message_freqs.keys()
        w = csv.writer(f)
        w.writerow(keys)
        for idx in range(len(time_periods)):
            line = []
            for key in keys:
                line.append(message_freqs[key][idx])
            w.writerow(line)
