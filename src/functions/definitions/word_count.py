import math

from src.functions import Function
from src.utils import helpers, constants

# TODO: total word count
average_word_count_category = "Average word count per message"


class WordCount(Function):
    @staticmethod
    def get_function_name():
        return "word_count"

    @staticmethod
    def get_categories():
        return [average_word_count_category]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [average_word_count_category]

    @staticmethod
    def process_messages_df(df, args):
        text = df["text"].astype("string")
        mt = df["message_type"].astype("string")
        not_reaction = ~mt.isin(constants.REACTION_TYPES)
        link_mask = text.str.match(constants.LINK_REGEX, na=False)
        df["is link?"] = (not_reaction & link_mask)
        # Handle missing values: .str.len() returns <NA> for missing → fill with 0
        df["word count"] = text.str.split().str.len().fillna(0).astype("int64")
        return df

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
        average_message_word_count = nr_messages[
            (nr_messages["word count"] != 0) & (~nr_messages["is link?"])
        ]["word count"].mean()
        if math.isnan(average_message_word_count):
            average_message_word_count = 0
        output_dict[average_word_count_category].append(
            round(average_message_word_count, 2)
        )
