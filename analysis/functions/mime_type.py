from analysis.functions import Function
from analysis.utils.constants import GRAPH_TOTAL_KEY
import analysis.utils.helpers as helpers

type_category = "Messages that are the selected file type"
percent_type_category = "Percent of messages that are the selected file type"


class MimeType(Function):
    @staticmethod
    def get_function_name():
        return "mime_type"

    @staticmethod
    def get_categories():
        return [type_category, percent_type_category]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [type_category, percent_type_category]

    @staticmethod
    def process_messages_df(df, args):
        mime_type = args.mime_type
        if mime_type is None:
            raise Exception("Function is type but not given a type")
        df[f"is file type {mime_type}?"] = df["type"].apply(
            lambda typ: helpers.is_type(typ, mime_type)
        )

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        mime_type = args.mime_type
        nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
        mime_type_messages = len(nr_messages[nr_messages[f"is file type {mime_type}?"]])
        output_dict[type_category].append(mime_type_messages)
        output_dict[percent_type_category].append(
            helpers.safe_divide_as_pct(mime_type_messages, len(nr_messages))
        )
