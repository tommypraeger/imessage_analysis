from src.functions import Function
from src.utils import helpers
import pandas as pd

all_caps_category = "Messages in all caps"
percent_all_caps_category = "Percent of messages that are in all caps"


class AllCaps(Function):
    @staticmethod
    def get_function_name():
        return "all_caps"

    @staticmethod
    def get_categories():
        return [all_caps_category, percent_all_caps_category]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [all_caps_category, percent_all_caps_category]

    @staticmethod
    def process_messages_df(df, args):
        text = df["text"].astype("string")
        letters = text.str.replace("[^a-zA-Z]", "", regex=True)
        non_empty = letters.str.len().gt(0).fillna(False)
        is_upper = letters.str.upper().eq(letters)
        df["is all caps?"] = non_empty & is_upper
        return df

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
        all_caps_messages = len(nr_messages[nr_messages["is all caps?"]])
        output_dict[all_caps_category].append(all_caps_messages)
        output_dict[percent_all_caps_category].append(
            helpers.safe_divide_as_pct(all_caps_messages, len(nr_messages))
        )
