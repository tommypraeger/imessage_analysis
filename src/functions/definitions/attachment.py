from src.functions import Function
from src.utils import helpers

attachment_category = "Messages that are attachments"
percent_attachment_category = "Percent of messages that are attachments"


class Attachment(Function):
    @staticmethod
    def get_function_name():
        return "attachment"

    @staticmethod
    def get_categories():
        return [attachment_category, percent_attachment_category]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [attachment_category, percent_attachment_category]

    @staticmethod
    def process_messages_df(df, args):
        df["is attachment?"] = df.apply(
            lambda msg: helpers.is_attachment(msg.text, msg.type), axis=1
        )

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
        attachment_messages = len(nr_messages[nr_messages["is attachment?"]])
        output_dict[attachment_category].append(attachment_messages)
        output_dict[percent_attachment_category].append(
            helpers.safe_divide_as_pct(attachment_messages, len(nr_messages))
        )
