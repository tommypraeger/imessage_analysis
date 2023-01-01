from analysis.utils.constants import GRAPH_TOTAL_KEY
import analysis.utils.helpers as helpers


def main(result_dict, df, chat_members, args):
    for member_name in chat_members:
        helpers.initialize_member(member_name, result_dict)


message_series_category = 'Total number of message series'
average_messages_category = 'Average messages per series'
percent_series_category = 'Percent of total message series'


def get_categories():
    return [
        message_series_category,
        average_messages_category,
        percent_series_category
    ]


def get_categories_allowing_graph_total():
    return [
        message_series_category,
        average_messages_category
    ]


def process_df(df, minutes_threshold):
    df['is conversation starter?'] = df['time'].diff().apply(
        lambda diff: helpers.is_conversation_starter(diff, minutes_threshold)
    )
    df.iloc[0, df.columns.get_loc('is conversation starter?')] = True
    df['is new message series?'] = df['sender'].apply(lambda x: True)
    df['is new message series?'] = df['is new message series?'].shift().where(
        df['sender'].shift() != df['sender'], False
    )
    df.iloc[0, df.columns.get_loc('is new message series?')] = True


def get_results(output_dict, df, member_name=None, time_period=None):
    messages = helpers.get_messages(df, member_name, time_period)
    message_series = len(messages[(messages['is new message series?'])
                                  | (messages['is conversation starter?'])])
    output_dict[message_series_category].append(message_series)
    output_dict[average_messages_category].append(
        round(helpers.safe_divide(len(messages), message_series), 2)
    )
    return message_series


def get_table_results(result_dict, df, chat_members, args):
    process_df(df, args.minutes_threshold)
    for member_name in chat_members:
        helpers.initialize_member(member_name, result_dict)
        get_results(result_dict, df, member_name)
    total_message_series = sum(result_dict[message_series_category])
    for i in range(len(result_dict[message_series_category])):
        result_dict[percent_series_category].append(
            round(helpers.safe_divide(result_dict[message_series_category]
                                      [i], total_message_series) * 100, 2))


def get_graph_results(graph_data, df, chat_members, time_periods, args):
    process_df(df, args.minutes_threshold)
    if args.graph_individual:
        get_individual_graph_results(graph_data, df, chat_members, time_periods)
    else:
        get_total_graph_results(graph_data, df, time_periods)


def get_individual_graph_results(graph_data, df, chat_members, time_periods):
    for time_period in time_periods:
        total_message_series_in_period = 0
        for member_name in chat_members:
            total_message_series_in_period += get_results(
                graph_data[member_name], df, member_name, time_period)
        for member_name in chat_members:
            graph_data[member_name][percent_series_category].append(
                round(helpers.safe_divide(graph_data[member_name][message_series_category][-1], total_message_series_in_period)
                      * 100, 2))


def get_total_graph_results(graph_data, df, time_periods):
    for time_period in time_periods:
        get_results(graph_data[GRAPH_TOTAL_KEY], df, None, time_period)
