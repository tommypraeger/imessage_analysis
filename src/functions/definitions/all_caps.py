from src.functions import Function
from src.utils import helpers

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
        df["is all caps?"] = df["text"].apply(helpers.is_all_caps)

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
        all_caps_messages = len(nr_messages[nr_messages["is all caps?"]])
        output_dict[all_caps_category].append(all_caps_messages)
        output_dict[percent_all_caps_category].append(
            helpers.safe_divide_as_pct(all_caps_messages, len(nr_messages))
        )
