from src.functions import Function
from src.utils import helpers

links_category = "Messages that are links"
percent_links_category = "Percent of messages that are links"


class Link(Function):
    @staticmethod
    def get_function_name():
        return "link"

    @staticmethod
    def get_categories():
        return [links_category, percent_links_category]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [links_category, percent_links_category]

    @staticmethod
    def process_messages_df(df, args):
        df["is link?"] = df.apply(
            lambda msg: helpers.is_link(msg.text, msg.message_type), axis=1
        )
        return df

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
        link_messages = len(nr_messages[nr_messages["is link?"]])
        output_dict[links_category].append(link_messages)
        output_dict[percent_links_category].append(
            helpers.safe_divide_as_pct(link_messages, len(nr_messages))
        )
