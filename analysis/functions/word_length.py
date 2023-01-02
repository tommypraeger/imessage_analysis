import math

from analysis.functions import Function
from analysis.utils.constants import GRAPH_TOTAL_KEY
import analysis.utils.helpers as helpers

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
        df["is attachment?"] = df["type"].apply(helpers.is_attachment)
        df["is link?"] = df["text"].apply(helpers.is_link)
        df["word count"] = df["text"].apply(helpers.message_word_count)
        df["letter count"] = df["text"].apply(helpers.message_letter_count)

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
        total_words = nr_messages[
            (~nr_messages["is attachment?"]) & (~nr_messages["is link?"])
        ]["word count"].sum()
        total_letters = nr_messages[
            (~nr_messages["is attachment?"]) & (~nr_messages["is link?"])
        ]["letter count"].sum()
        average_word_length = round(helpers.safe_divide(total_letters, total_words), 1)
        if math.isnan(average_word_length):
            average_word_length = 0
        output_dict[average_word_length_category].append(average_word_length)
