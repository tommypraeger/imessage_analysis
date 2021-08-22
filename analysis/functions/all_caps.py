import analysis.utils.constants as constants
import analysis.utils.helpers as helpers

all_caps_column = 'all caps messages'
percent_all_caps_column = '% of messages that are all caps'


def get_columns():
    return [
        all_caps_column,
        percent_all_caps_column
    ]


def get_columns_allowing_graph_total():
    return [
        all_caps_column
    ]


def get_table_results(result_dict, df, chat_members, args=None):
    df['is all caps?'] = df['text'].apply(helpers.is_all_caps)
    for member_name in chat_members:
        helpers.initialize_member(member_name, df, result_dict)
        non_reaction_messages = helpers.get_non_reaction_messages_for_member(df, member_name)
        all_caps_messages = len(
            df[(df['is all caps?']) & (df['sender'] == member_name)]
        )
        result_dict[all_caps_column].append(all_caps_messages)
        result_dict[percent_all_caps_column].append(
            round(helpers.safe_divide(all_caps_messages, non_reaction_messages) * 100, 2)
        )


def get_graph_results(graph_data, df, chat_members, time_periods, args):
    df['is all caps?'] = df['text'].apply(helpers.is_all_caps)
    if args.graph_individual:
        get_individual_graph_data(graph_data, df, chat_members, time_periods)
    else:
        get_total_graph_data(graph_data, df, time_periods)


def get_individual_graph_data(graph_data, df, chat_members, time_periods):
    for time_period in time_periods:
        for member_name in chat_members:
            non_reaction_messages = helpers.get_non_reaction_messages_for_member(
                df, member_name, time_period)
            all_caps_messages = len(
                df[(df['is all caps?'])
                   & (df['time_period'] == time_period)
                   & (df['sender'] == member_name)]
            )
            graph_data[member_name][all_caps_column].append(all_caps_messages)
            graph_data[member_name][percent_all_caps_column].append(
                round(helpers.safe_divide(all_caps_messages, non_reaction_messages) * 100, 2))


def get_total_graph_data(graph_data, df, time_periods):
    for time_period in time_periods:
        graph_data['Total'][all_caps_column].append(len(
            df[(df['is all caps?']) & (df['time_period'] == time_period)]
        ))
