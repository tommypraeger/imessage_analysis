import math

from src.functions import Function
from src.utils import helpers, constants

average_word_count_category = "Average word count per message"
total_word_count_category = "Total word count"


def add_word_count_columns(df):
    text = df["text"].astype("string")
    mt = df["message_type"].astype("string")
    not_reaction = ~mt.isin(constants.REACTION_TYPES)
    link_only_mask = text.str.strip().str.fullmatch(constants.LINK_REGEX, na=False)
    df["is link?"] = (not_reaction & link_only_mask)
    # Handle missing values: .str.len() returns <NA> for missing → fill with 0
    df["word count"] = text.str.split().str.len().fillna(0).astype("int64")
    return df


def total_word_count_by_sender(df, member_name=None, time_period=None):
    """Aggregate total word count per sender, excluding reactions and link-only messages."""

    nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
    working = nr_messages
    if "word count" not in working.columns or "is link?" not in working.columns:
        working = add_word_count_columns(working.copy())

    mask = (working["word count"] != 0) & (~working["is link?"])
    return (
        working.loc[mask]
        .groupby("sender")["word count"]
        .sum()
        .astype("int64")
        .to_dict()
    )


class WordCount(Function):
    @staticmethod
    def get_function_name():
        return "word_count"

    @staticmethod
    def get_categories():
        return [average_word_count_category, total_word_count_category]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [average_word_count_category, total_word_count_category]

    @staticmethod
    def process_messages_df(df, args):
        return add_word_count_columns(df)

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
        totals_by_sender = total_word_count_by_sender(df, member_name, time_period)
        if member_name is None:
            total_words = int(sum(totals_by_sender.values()))
        else:
            total_words = int(totals_by_sender.get(member_name, 0))
        output_dict[total_word_count_category].append(total_words)
