from analysis.utils.constants import GRAPH_TOTAL_KEY
import analysis.utils.helpers as helpers

type_category = 'Messages that are the selected file type'
percent_type_category = 'Percent of messages that are the selected file type'


def get_categories():
    return [
        type_category,
        percent_type_category
    ]


def get_categories_allowing_graph_total():
    return [
        type_category,
        percent_type_category
    ]


def process_df(df, mime_type):
    if mime_type is None:
        raise Exception('Function is type but not given a type')
    df[f'is file type {mime_type}?'] = df['type'].apply(lambda typ: helpers.is_type(typ, mime_type))


def get_results(output_dict, df, mime_type, member_name=None, time_period=None):
    nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
    mime_type_messages = len(nr_messages[nr_messages[f'is file type {mime_type}?']])
    output_dict[type_category].append(mime_type_messages)
    output_dict[percent_type_category].append(
        round(helpers.safe_divide(mime_type_messages, len(nr_messages)) * 100, 2))


def get_table_results(result_dict, df, chat_members, args):
    mime_type = args.mime_type
    process_df(df, mime_type)
    for member_name in chat_members:
        helpers.initialize_member(member_name, result_dict)
        get_results(result_dict, df, mime_type, member_name)


def get_graph_results(graph_data, df, chat_members, time_periods, args):
    mime_type = args.mime_type
    process_df(df, mime_type)
    if args.graph_individual:
        get_individual_graph_results(graph_data, df, mime_type, chat_members, time_periods)
    else:
        get_total_graph_results(graph_data, df, mime_type, time_periods)


def get_individual_graph_results(graph_data, df, mime_type, chat_members, time_periods):
    for time_period in time_periods:
        for member_name in chat_members:
            get_results(graph_data[member_name], df, mime_type, member_name, time_period)


def get_total_graph_results(graph_data, df, mime_type, time_periods):
    for time_period in time_periods:
        get_results(graph_data[GRAPH_TOTAL_KEY], df, mime_type, None, time_period)
