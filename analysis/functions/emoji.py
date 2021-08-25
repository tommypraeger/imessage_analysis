from analysis.utils.constants import GRAPH_TOTAL_KEY
import analysis.utils.helpers as helpers

emoji_column = 'Messages that contain emoji'
percent_emoji_column = 'Percent of messages that contain emoji'


def get_columns():
    return [
        emoji_column,
        percent_emoji_column
    ]


def get_columns_allowing_graph_total():
    return [
        emoji_column,
        percent_emoji_column
    ]


def process_df(df):
    df['includes emoji?'] = df['text'].apply(helpers.includes_emoji)


def get_results(output_dict, df, member_name=None, time_period=None):
    nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
    emoji_messages = len(nr_messages[nr_messages['includes emoji?']])
    output_dict[emoji_column].append(emoji_messages)
    output_dict[percent_emoji_column].append(
        round(helpers.safe_divide(emoji_messages, len(nr_messages)) * 100, 2))


def get_table_results(result_dict, df, chat_members, args):
    process_df(df)
    for member_name in chat_members:
        helpers.initialize_member(member_name, result_dict)
        get_results(result_dict, df, member_name)


def get_graph_results(graph_data, df, chat_members, time_periods, args):
    process_df(df)
    if args.graph_individual:
        get_individual_graph_results(graph_data, df, chat_members, time_periods)
    else:
        get_total_graph_results(graph_data, df, time_periods)


def get_individual_graph_results(graph_data, df, chat_members, time_periods):
    for time_period in time_periods:
        for member_name in chat_members:
            get_results(graph_data[member_name], df, member_name, time_period)


def get_total_graph_results(graph_data, df, time_periods):
    for time_period in time_periods:
        get_results(graph_data[GRAPH_TOTAL_KEY], df, None, time_period)
