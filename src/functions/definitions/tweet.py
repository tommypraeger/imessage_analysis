from src.functions import Function
from src.utils import helpers

tweets_category = "Messages that are tweets"
percent_tweets_category = "Percent of messages that are tweets"


class Tweet(Function):
    @staticmethod
    def get_function_name():
        return "tweet"

    @staticmethod
    def get_categories():
        return [tweets_category, percent_tweets_category]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [tweets_category, percent_tweets_category]

    @staticmethod
    def process_messages_df(df, args):
        df["is tweet?"] = df.apply(
            lambda msg: helpers.is_tweet(msg.text, msg.reaction_type), axis=1
        )

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
        tweet_messages = len(nr_messages[nr_messages["is tweet?"]])
        output_dict[tweets_category].append(tweet_messages)
        output_dict[percent_tweets_category].append(
            helpers.safe_divide_as_pct(tweet_messages, len(nr_messages))
        )
