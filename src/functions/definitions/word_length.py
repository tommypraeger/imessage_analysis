import math
import re

from src.functions import Function
from src.functions.definitions.word_count import add_word_count_columns
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
        df = add_word_count_columns(df)
        text = df["text"].astype("string")
        # Letters only: strip non-letters then length
        letters = text.str.replace("[^a-zA-Z]+", "", regex=True)
        df["letter count"] = letters.str.len().fillna(0).astype("int64")
        return df

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
        words_series = nr_messages["text"].astype("string").str.split()

        def is_valid_word(word: str) -> bool:
            if len(word) > 20:
                return False
            if re.search(r"(.)\\1{4}", word):
                return False
            return True

        def clean_letters(word: str) -> str:
            return re.sub(r"[^a-zA-Z]+", "", word)

        filtered_words = words_series.apply(
            lambda words: [w for w in words if is_valid_word(w)] if isinstance(words, list) else []
        )
        filtered_counts = filtered_words.apply(len)
        filtered_letters = filtered_words.apply(lambda ws: sum(len(clean_letters(w)) for w in ws if clean_letters(w)))

        mask = (~nr_messages["is link?"]) & (filtered_counts > 0)

        total_words = filtered_counts[mask].sum()
        total_letters = filtered_letters[mask].sum()
        average_word_length = round(helpers.safe_divide(total_letters, total_words), 2)
        if math.isnan(average_word_length):
            average_word_length = 0
        output_dict[average_word_length_category].append(average_word_length)
