from analysis.utils.constants import GRAPH_TOTAL_KEY
import analysis.utils.helpers as helpers

total_messages_column = 'Total messages'
percent_total_messages_column = 'Percent of total messages'


def get_columns():
    return [
        total_messages_column,
        percent_total_messages_column
    ]


def get_columns_allowing_graph_total():
    return [
        total_messages_column
    ]


def get_results(output_dict, df, member_name=None, time_period=None):
    total_messages_by_member = helpers.get_total_messages(df, member_name, time_period)
    output_dict[total_messages_column].append(total_messages_by_member)
    return total_messages_by_member


def get_table_results(result_dict, df, chat_members, args):
    for member_name in chat_members:
        helpers.initialize_member(member_name, result_dict)
        get_results(result_dict, df, member_name)
    total_messages = sum(result_dict[total_messages_column])
    for i in range(len(result_dict[total_messages_column])):
        result_dict[percent_total_messages_column].append(
            round(helpers.safe_divide(
                result_dict[total_messages_column][i], total_messages) * 100, 2)
        )


def get_graph_results(graph_data, df, chat_members, time_periods, args):
    if args.graph_individual:
        get_individual_graph_results(graph_data, df, chat_members, time_periods)
    else:
        get_total_graph_results(graph_data, df, time_periods)


def get_individual_graph_results(graph_data, df, chat_members, time_periods):
    for time_period in time_periods:
        total_messages_in_period = 0
        for member_name in chat_members:
            total_messages_in_period += get_results(
                graph_data[member_name], df, member_name, time_period)
        for member_name in chat_members:
            graph_data[member_name][percent_total_messages_column].append(
                round(helpers.safe_divide(
                    graph_data[member_name][total_messages_column][-1],
                    total_messages_in_period) * 100, 2))


def get_total_graph_results(graph_data, df, time_periods):
    for time_period in time_periods:
        get_results(graph_data[GRAPH_TOTAL_KEY], df, None, time_period)
