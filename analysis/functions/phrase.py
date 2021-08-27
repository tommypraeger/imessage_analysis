from analysis.utils.constants import GRAPH_TOTAL_KEY
import analysis.utils.helpers as helpers

phrase_category = 'Messages that contain the entered phrase'
percent_phrase_category = 'Percent of messages that contain the entered phrase'


def get_categories():
    return [
        phrase_category,
        percent_phrase_category
    ]


def get_categories_allowing_graph_total():
    return [
        phrase_category,
        percent_phrase_category
    ]


def process_df(df, phrase, case_sensitive, separate, regex):
    if phrase is None:
        raise Exception('Function is phrase but not given a phrase')
    df[f'includes {phrase}?'] = df['text'].apply(
        lambda msg: helpers.is_phrase_in(phrase, msg, case_sensitive, separate, regex)
    )


def get_results(output_dict, df, phrase, member_name=None, time_period=None):
    nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
    phrase_messages = len(nr_messages[nr_messages[f'includes {phrase}?']])
    output_dict[phrase_category].append(phrase_messages)
    output_dict[percent_phrase_category].append(
        round(helpers.safe_divide(phrase_messages, len(nr_messages)) * 100, 2))


def get_table_results(result_dict, df, chat_members, args):
    phrase = args.phrase
    process_df(df, phrase, args.case_sensitive, args.separate, args.regex)
    for member_name in chat_members:
        helpers.initialize_member(member_name, result_dict)
        get_results(result_dict, df, phrase, member_name)


def get_graph_results(graph_data, df, chat_members, time_periods, args):
    phrase = args.phrase
    process_df(df, phrase, args.case_sensitive, args.separate, args.regex)
    if args.graph_individual:
        get_individual_graph_results(graph_data, df, phrase, chat_members, time_periods)
    else:
        get_total_graph_results(graph_data, df, phrase, time_periods)


def get_individual_graph_results(graph_data, df, phrase, chat_members, time_periods):
    for time_period in time_periods:
        for member_name in chat_members:
            get_results(graph_data[member_name], df, phrase, member_name, time_period)


def get_total_graph_results(graph_data, df, phrase, time_periods):
    for time_period in time_periods:
        get_results(graph_data[GRAPH_TOTAL_KEY], df, phrase, None, time_period)
