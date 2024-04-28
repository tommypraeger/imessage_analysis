from src.functions import Function
from src.utils import helpers

phrase_category = "Messages that contain the entered phrase"
percent_phrase_category = "Percent of messages that contain the entered phrase"


class Phrase(Function):
    @staticmethod
    def get_function_name():
        return "phrase"

    @staticmethod
    def get_categories():
        return [phrase_category, percent_phrase_category]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [phrase_category, percent_phrase_category]

    @staticmethod
    def process_messages_df(df, args):
        phrase = args.phrase
        case_sensitive = args.case_sensitive
        separate = args.separate
        regex = args.regex
        if phrase is None:
            raise Exception("Function is phrase but not given a phrase")
        df[f"includes {phrase}?"] = df.apply(
            lambda msg: helpers.is_phrase_in(
                phrase, msg.text, msg.reaction_type, case_sensitive, separate, regex
            ),
            axis=1
        )

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        phrase = args.phrase
        nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
        phrase_messages = len(nr_messages[nr_messages[f"includes {phrase}?"]])
        output_dict[phrase_category].append(phrase_messages)
        output_dict[percent_phrase_category].append(
            round(helpers.safe_divide(phrase_messages, len(nr_messages)) * 100, 2)
        )
