from analysis.utils.constants import GRAPH_TOTAL_KEY
import analysis.utils.helpers as helpers

tweets_category = 'Messages that are tweets'
percent_tweets_category = 'Percent of messages that are tweets'


def get_categories():
    return [
        tweets_category,
        percent_tweets_category
    ]


def get_categories_allowing_graph_total():
    return [
        tweets_category,
        percent_tweets_category
    ]


def process_df(df):
    df['is tweet?'] = df['text'].apply(helpers.is_tweet)


def get_results(output_dict, df, member_name=None, time_period=None):
    nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
    tweet_messages = len(nr_messages[nr_messages['is tweet?']])
    output_dict[tweets_category].append(tweet_messages)
    output_dict[percent_tweets_category].append(
        round(helpers.safe_divide(tweet_messages, len(nr_messages)) * 100, 2))


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
