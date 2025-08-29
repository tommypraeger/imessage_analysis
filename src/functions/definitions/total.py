from src.functions import Function
from src.utils import helpers

total_messages_category = "Total messages"
percent_total_messages_category = "Percent of total messages"


class Total(Function):
    @staticmethod
    def get_function_name():
        return "total"

    @staticmethod
    def get_categories():
        return [total_messages_category, percent_total_messages_category]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [total_messages_category]

    @staticmethod
    def process_messages_df(df, args):
        return df  # no processing necessary

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        # Exclude reactions from total messages
        total_messages_by_member = helpers.get_total_non_reaction_messages(
            df, member_name, time_period
        )
        output_dict[total_messages_category].append(total_messages_by_member)
        total_messages = helpers.get_total_non_reaction_messages(
            df, time_period=time_period
        )
        output_dict[percent_total_messages_category].append(
            round(
                helpers.safe_divide(total_messages_by_member, total_messages) * 100,
                2,
            )
        )
