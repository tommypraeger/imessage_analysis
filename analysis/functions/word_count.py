import math

from analysis.utils.constants import GRAPH_TOTAL_KEY
import analysis.utils.helpers as helpers

average_word_count_category = 'Average word count per message'


def get_categories():
    return [
        average_word_count_category
    ]


def get_categories_allowing_graph_total():
    return [
        average_word_count_category
    ]


def process_df(df):
    df['is attachment?'] = df['type'].apply(helpers.is_attachment)
    df['is link?'] = df['text'].apply(helpers.is_link)
    df['word count'] = df['text'].apply(helpers.message_word_count)


def get_results(output_dict, df, member_name=None, time_period=None):
    nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
    average_message_word_count = nr_messages[
        (~nr_messages['is attachment?']) & (~nr_messages['is link?'])
    ]['word count'].mean()
    if math.isnan(average_message_word_count):
        average_message_word_count = 0
    output_dict[average_word_count_category].append(round(average_message_word_count, 1))


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
