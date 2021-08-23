from analysis.utils.constants import GRAPH_TOTAL_KEY
import analysis.utils.helpers as helpers

attachment_column = 'Messages that are attachments'
percent_attachment_column = 'Percent of messages that are attachments'


def get_columns():
    return [
        attachment_column,
        percent_attachment_column
    ]


def get_columns_allowing_graph_total():
    return [
        attachment_column,
        percent_attachment_column
    ]


def get_table_results(result_dict, df, chat_members, args=None):
    df['is attachment?'] = df['type'].apply(helpers.is_attachment)
    for member_name in chat_members:
        helpers.initialize_member(member_name, result_dict)
        nr_messages = helpers.get_non_reaction_messages(df, member_name)
        attachment_messages = len(nr_messages[nr_messages['is attachment?']])
        result_dict[attachment_column].append(attachment_messages)
        result_dict[percent_attachment_column].append(
            round(helpers.safe_divide(attachment_messages, len(nr_messages)) * 100, 2))


def get_graph_results(graph_data, df, chat_members, time_periods, args):
    df['is attachment?'] = df['type'].apply(helpers.is_attachment)
    if args.graph_individual:
        get_individual_graph_data(graph_data, df, chat_members, time_periods)
    else:
        get_total_graph_data(graph_data, df, time_periods)


def get_individual_graph_data(graph_data, df, chat_members, time_periods):
    for time_period in time_periods:
        for member_name in chat_members:
            nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
            attachment_messages = len(nr_messages[nr_messages['is attachment?']])
            graph_data[member_name][attachment_column].append(attachment_messages)
            graph_data[member_name][percent_attachment_column].append(
                round(helpers.safe_divide(attachment_messages, len(nr_messages)) * 100, 2))


def get_total_graph_data(graph_data, df, time_periods):
    for time_period in time_periods:
        nr_messages = helpers.get_non_reaction_messages(df, time_period=time_period)
        attachment_messages = len(nr_messages[nr_messages['is attachment?']])
        graph_data[GRAPH_TOTAL_KEY][attachment_column].append(attachment_messages)
        graph_data[GRAPH_TOTAL_KEY][percent_attachment_column].append(
            round(helpers.safe_divide(attachment_messages, len(nr_messages)) * 100, 2))
