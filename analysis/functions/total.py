import analysis.utils.constants as constants
import analysis.utils.helpers as helpers

total_messages_column = 'Total Messages'
percent_total_messages_column = 'Percent of Total Messages'


def get_columns():
    return [
        total_messages_column,
        percent_total_messages_column
    ]


def get_columns_allowing_graph_total():
    return [
        total_messages_column
    ]


def get_table_results(result_dict, df, chat_members, args=None):
    for column in get_columns():
        result_dict[column] = []

    for member_name in chat_members:
        helpers.initialize_member(member_name, df, result_dict)
        total_messages_by_member = helpers.get_total_messages_for_member(df, member_name)
        result_dict[total_messages_column].append(total_messages_by_member)
    total_messages = sum(result_dict[total_messages_column])
    for i in range(len(result_dict[total_messages_column])):
        result_dict[percent_total_messages_column].append(
            round(helpers.safe_divide(
                result_dict[total_messages_column][i], total_messages) * 100, 2)
        )


def get_graph_results(graph_data, df, chat_members, time_periods, args):
    if args.graph_individual:
        for member_name in chat_members:
            for column in get_columns():
                graph_data[member_name][column] = []
        get_individual_graph_data(graph_data, df, chat_members, time_periods)
    else:
        for column in get_columns_allowing_graph_total():
            graph_data['Total'][column] = []
        get_total_graph_data(graph_data, df, time_periods)


def get_individual_graph_data(graph_data, df, chat_members, time_periods):
    for time_period in time_periods:
        total_messages_in_period = 0
        for member_name in chat_members:
            total_messages_by_member = len(
                df[(df['time_period'] == time_period) & (df['sender'] == member_name)]
            )
            graph_data[member_name][total_messages_column].append(total_messages_by_member)
            total_messages_in_period += total_messages_by_member
        for member_name in chat_members:
            graph_data[member_name][percent_total_messages_column].append(
                round(helpers.safe_divide(graph_data[member_name][total_messages_column][-1], total_messages_in_period)
                      * 100,
                      2)
            )


def get_total_graph_data(graph_data, df, time_periods):
    for time_period in time_periods:
        graph_data['Total'][total_messages_column].append(len(
            df[df['time_period'] == time_period]
        ))
