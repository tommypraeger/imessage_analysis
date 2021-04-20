import csv
import datetime
import os
import time

#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates

from analysis.utils.initialize_result_dict import initialize_result_dict
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers


def main(result_dict, df, chat_members, args):
    if not (args.day or args.week or args.month or args.year):
        raise Exception('Must give time period length for graph')

    message_freqs = {}
    if args.graph_individual:
        members = []
        for member_name in chat_members:
            total_messages, _ = initialize_result_dict(
                member_name, df, result_dict)
            if total_messages > 0:
                members.append(member_name)
        for member in members:
            message_freqs[member] = []
    else:
        message_freqs['Total Messages'] = []

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
        if args.graph_individual:
            for member_name in members:
                message_freqs[member_name].append(len(
                    df[(df['time_period'] == time_period) & (df['sender'] == member_name)]
                ))
        else:
            message_freqs['Total Messages'].append(len(
                df[df['time_period'] == time_period]
            ))

    colors = [
        'rgba(31, 120, 180, 1)',
        'rgba(51, 160, 44, 1)',
        'rgba(227, 26, 28, 1)',
        'rgba(255, 127, 0, 1)',
        'rgba(106, 61, 154, 1)',
        'rgba(177, 89, 40, 1)',
        'rgba(166, 206, 227, 1)',
        'rgba(178, 223, 138, 1)',
        'rgba(251, 154, 153, 1)',
        'rgba(253, 191, 111, 1)',
        'rgba(202, 178, 214, 1)',
        'rgba(255, 255, 153, 1)'
    ]

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
            'borderColor': colors[i % len(message_freqs)]
        }
        for i, name in enumerate(message_freqs)
    ]

    # fig, ax = plt.subplots()

    # x = [datetime.datetime.strptime(d, day_fmt).date() for d in time_periods]

    # for key in message_freqs:
    #     ax.plot(x, message_freqs[key], label=key)

    # if args.day or args.week:
    #     ax.xaxis.set_major_formatter(mdates.DateFormatter(day_fmt))
    #     ax.xaxis.set_major_locator(mdates.DayLocator())
    # elif args.month:
    #     ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
    #     ax.xaxis.set_major_locator(mdates.MonthLocator())
    # elif args.year:
    #     ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    #     ax.xaxis.set_major_locator(mdates.YearLocator())
    #     ax.xaxis.set_minor_locator(mdates.MonthLocator())

    # num_ticks = 16 if len(time_periods) > 16 else len(time_periods)
    # ax.xaxis.set_major_locator(plt.MaxNLocator(num_ticks))
    # fig.autofmt_xdate()

    # ax.set_title(f'{args.name}, by {time_period_name}')
    # ax.set_xlabel('Date')
    # ax.set_ylabel('# of Messages')
    # ax.legend()
    # time_stamp = int(time.time())
    # os.system('rm ui/public/graph_*.png')
    # image_path = f'ui/public/graph_{time_stamp}.png'
    # plt.savefig(image_path, bbox_inches='tight')
    # result_dict['imagePath'] = image_path.split('/')[-1]

    # message_freqs['Date'] = []
    # for time_period in time_periods:
    #     message_freqs['Date'].append(time_period)
    # csv_file = 'message_frequencies.csv'
    # with open(csv_file, 'w') as f:
    #     keys = message_freqs.keys()
    #     w = csv.writer(f)
    #     w.writerow(keys)
    #     for idx in range(len(time_periods)):
    #         line = []
    #         for key in keys:
    #             line.append(message_freqs[key][idx])
    #         w.writerow(line)
