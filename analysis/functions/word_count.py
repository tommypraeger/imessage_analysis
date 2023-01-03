import math

from analysis.functions import Function
from analysis.utils.constants import GRAPH_TOTAL_KEY
import analysis.utils.helpers as helpers

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
        df["is link?"] = df["text"].apply(helpers.is_link)
        df["word count"] = df["text"].apply(helpers.message_word_count)

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
