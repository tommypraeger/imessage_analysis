import datetime
from dateutil import relativedelta

import analysis.functions.all_caps as all_caps
import analysis.functions.attachment as attachment
import analysis.functions.conversation_starter as conversation_starter
import analysis.functions.emoji as emoji
import analysis.functions.game as game
import analysis.functions.link as link
import analysis.functions.message_series as message_series
import analysis.functions.mime_type as mime_type
import analysis.functions.phrase as phrase
import analysis.functions.reaction as reaction
import analysis.functions.total as total
import analysis.functions.tweet as tweet
import analysis.functions.word_count as word_count
import analysis.functions.word_length as word_length
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers

function_to_class_map = {
    'total': total,
    'reaction': reaction,
    'attachment': attachment,
    'emoji': emoji,
    'all_caps': all_caps,
    'conversation_starter': conversation_starter,
    'tweet': tweet,
    'link': link,
    'word_count': word_count,
    'word_length': word_length,
    'message_series': message_series,
    'game': game,
    'phrase': phrase,
    'mime_type': mime_type
}


def process_df(df, args, chat_members):
    function = args.function
    function_class = function_to_class_map[function]

    result_dict = {}

    if args.table:
        result_dict['names'] = []
        for column in function_class.get_columns():
            result_dict[column] = []
        function_class.get_table_results(result_dict, df, chat_members, args)

    elif args.graph:
        # set up
        graph_data = {}
        set_up_graph_data(graph_data, args, chat_members, df, function)
        add_time_period_to_df(df, args.graph_time_interval)
        time_periods = get_time_periods(df, args.graph_time_interval)

        # get graph data
        function_class.get_graph_results(
            graph_data, df, chat_members, time_periods, args)

        # prepare to return data
        format_graph_data(result_dict, graph_data, time_periods,
                          args.column, args.graph_time_interval)

    return result_dict


def set_up_graph_data(graph_data, args, chat_members, df, function_class):
    columns = function_class.get_columns()
    columns_allowing_graph_total = function_class.get_columns_allowing_graph_total()
    if args.graph_individual:
        for member_name in chat_members:
            graph_data[member_name] = {}
            for column in columns:
                graph_data[member_name][column] = []
    else:
        graph_data['Total'] = {}
        for column in columns_allowing_graph_total:
            graph_data['Total'][column] = []


def add_time_period_to_df(df, graph_time_interval):
    if graph_time_interval == 'day':
        df['time_period'] = df['time'].apply(helpers.get_day)
    elif graph_time_interval == 'week':
        df['time_period'] = df['time'].apply(helpers.get_week)
    elif graph_time_interval == 'month':
        df['time_period'] = df['time'].apply(helpers.get_month)
    elif graph_time_interval == 'year':
        df['time_period'] = df['time'].apply(helpers.get_year)


def format_graph_data(result_dict, graph_data, time_periods, column, graph_time_interval):
    if graph_time_interval == 'day' or graph_time_interval == 'week':
        result_dict['labels'] = time_periods
    elif graph_time_interval == 'month':
        result_dict['labels'] = [
            f'{time_period.split("/")[0]}/{time_period.split("/")[2]}'
            for time_period in time_periods
        ]
    elif graph_time_interval == 'year':
        result_dict['labels'] = [
            f'20{time_period.split("/")[2]}'
            for time_period in time_periods
        ]

    result_dict['datasets'] = [
        {
            'label': name,
            'data': graph_data[name][column],
            'fill': False,
            'borderColor': constants.GRAPH_COLORS[i % len(graph_data)]
        }
        for i, name in enumerate(graph_data)
    ]


def get_time_periods(df, time_period_name):
    day_fmt = '%m/%d/%y'
    begin_date = datetime.datetime.strptime(df['time_period'].iloc[0], day_fmt)
    end_date = datetime.datetime.strptime(df['time_period'].iloc[-1], day_fmt)

    if time_period_name == 'day':
        num_days = (end_date - begin_date).days
        return [
            helpers.get_day(begin_date + relativedelta.relativedelta(days=i))
            for i in range(num_days + 1)
        ]
    if time_period_name == 'week':
        num_weeks = (end_date - begin_date).days // 7
        return [
            helpers.get_week(begin_date + relativedelta.relativedelta(days=i*7))
            for i in range(num_weeks + 1)
        ]
    if time_period_name == 'month':
        num_months = (end_date.year - begin_date.year) * 12 + (end_date.month - begin_date.month)
        return [
            helpers.get_month(begin_date + relativedelta.relativedelta(months=i))
            for i in range(num_months + 1)
        ]
    if time_period_name == 'year':
        num_years = end_date.year - begin_date.year
        return [
            helpers.get_year(begin_date + relativedelta.relativedelta(years=i))
            for i in range(num_years + 1)
        ]
