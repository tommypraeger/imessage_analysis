from analysis.utils.constants import GRAPH_TOTAL_KEY
import analysis.utils.helpers as helpers

all_caps_column = 'Messages in all caps'
percent_all_caps_column = 'Percent of messages that are in all caps'


def get_columns():
    return [
        all_caps_column,
        percent_all_caps_column
    ]


def get_columns_allowing_graph_total():
    return [
        all_caps_column,
        percent_all_caps_column
    ]


def get_table_results(result_dict, df, chat_members, args=None):
    df['is all caps?'] = df['text'].apply(helpers.is_all_caps)
    for member_name in chat_members:
        helpers.initialize_member(member_name, result_dict)
        nr_messages = helpers.get_non_reaction_messages(df, member_name)
        all_caps_messages = len(nr_messages[nr_messages['is all caps?']])
        result_dict[all_caps_column].append(all_caps_messages)
        result_dict[percent_all_caps_column].append(
            round(helpers.safe_divide(all_caps_messages, len(nr_messages)) * 100, 2))


def get_graph_results(graph_data, df, chat_members, time_periods, args):
    df['is all caps?'] = df['text'].apply(helpers.is_all_caps)
    if args.graph_individual:
        get_individual_graph_data(graph_data, df, chat_members, time_periods)
    else:
        get_total_graph_data(graph_data, df, time_periods)


def get_individual_graph_data(graph_data, df, chat_members, time_periods):
    for time_period in time_periods:
        for member_name in chat_members:
            nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
            all_caps_messages = len(nr_messages[nr_messages['is all caps?']])
            graph_data[member_name][all_caps_column].append(all_caps_messages)
            graph_data[member_name][percent_all_caps_column].append(
                round(helpers.safe_divide(all_caps_messages, len(nr_messages)) * 100, 2))


def get_total_graph_data(graph_data, df, time_periods):
    for time_period in time_periods:
        nr_messages = helpers.get_non_reaction_messages(df, time_period=time_period)
        all_caps_messages = len(nr_messages[nr_messages['is all caps?']])
        graph_data[GRAPH_TOTAL_KEY][all_caps_column].append(all_caps_messages)
        graph_data[GRAPH_TOTAL_KEY][percent_all_caps_column].append(
            round(helpers.safe_divide(all_caps_messages, len(nr_messages)) * 100, 2))
