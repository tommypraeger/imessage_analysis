import csv
import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from analysis.utils.initialize_result_dict import initialize_result_dict
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers


def main(result_dict, df, chat_members, args):
    if not (args.day or args.week or args.month or args.year):
        raise Exception('Must give time period length for graph')

    message_freqs = {
        'Total': []
    }
    if args.graph_individual:
        members = []
        for member_name in chat_members:
            total_messages, non_reaction_messages = initialize_result_dict(
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
        message_freqs['Total'].append(len(
            df[df['time_period'] == time_period]
        ))
        if args.graph_individual:
            for member_name in members:
                message_freqs[member_name].append(len(
                    df[(df['time_period'] == time_period) & (df['sender'] == member_name)]
                ))

    plt.figure()

    x = [datetime.datetime.strptime(d, day_fmt).date() for d in time_periods]
    ax = plt.gca()

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

    for key in message_freqs:
        plt.plot(x, message_freqs[key], label=key)

    max_ticks = 15 if args.month or args.year else 10
    if len(x) > max_ticks:
        ax.xaxis.set_major_locator(plt.MaxNLocator(max_ticks))

    plt.title(f'{args.name}, by {time_period_name}')
    plt.xlabel('Date')
    plt.ylabel('# of Messages')
    plt.legend()
    plt.savefig('ui/public/graph.png', bbox_inches='tight')

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
