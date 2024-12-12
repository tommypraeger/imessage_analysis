from src.functions import Function
from src.utils import helpers

emoji_category = "Messages that contain emoji"
percent_emoji_category = "Percent of messages that contain emoji"


class Emoji(Function):
    @staticmethod
    def get_function_name():
        return "emoji"

    @staticmethod
    def get_categories():
        return [emoji_category, percent_emoji_category]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [emoji_category, percent_emoji_category]

    @staticmethod
    def process_messages_df(df, args):
        df["includes emoji?"] = df.apply(
            lambda msg: helpers.includes_emoji(msg.text, msg.message_type), axis=1
        )
        return df

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
        emoji_messages = len(nr_messages[nr_messages["includes emoji?"]])
        output_dict[emoji_category].append(emoji_messages)
        output_dict[percent_emoji_category].append(
            helpers.safe_divide_as_pct(emoji_messages, len(nr_messages))
        )
