import math

from src.functions import Function
from src.utils import helpers, constants

average_word_length_category = "Average letters per word"


class WordLength(Function):
    @staticmethod
    def get_function_name():
        return "word_length"

    @staticmethod
    def get_categories():
        return [average_word_length_category]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [average_word_length_category]

    @staticmethod
    def process_messages_df(df, args):
        text = df["text"].astype("string")
        mt = df["message_type"].astype("string")
        not_reaction = ~mt.isin(constants.REACTION_TYPES)
        link_mask = text.str.match(constants.LINK_REGEX, na=False)
        df["is link?"] = (not_reaction & link_mask)
        df["word count"] = text.str.split().str.len().fillna(0).astype("int64")
        # Letters only: strip non-letters then length
        letters = text.str.replace("[^a-zA-Z]+", "", regex=True)
        df["letter count"] = letters.str.len().fillna(0).astype("int64")
        return df

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
        total_words = nr_messages[
            (nr_messages["word count"] != 0) & (~nr_messages["is link?"])
        ]["word count"].sum()
        total_letters = nr_messages[
            (nr_messages["word count"] != 0) & (~nr_messages["is link?"])
        ]["letter count"].sum()
        average_word_length = round(helpers.safe_divide(total_letters, total_words), 2)
        if math.isnan(average_word_length):
            average_word_length = 0
        output_dict[average_word_length_category].append(average_word_length)
