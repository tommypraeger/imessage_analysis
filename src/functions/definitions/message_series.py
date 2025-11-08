from src.functions import Function
from src.utils import helpers, constants


message_series_category = "Total number of message series"
average_messages_category = "Average messages per series"
percent_series_category = "Percent of total message series"


class MessageSeries(Function):
    @staticmethod
    def get_function_name():
        return "message_series"

    @staticmethod
    def get_categories():
        return [
            message_series_category,
            average_messages_category,
            percent_series_category,
        ]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [
            message_series_category,
            average_messages_category
        ]

    @staticmethod
    def process_messages_df(df, args):
        # Populate conversation columns using the shared helper so that
        # reactions never start conversations and inherit parent conversations.
        df = helpers.compute_conversation_columns(
            df,
            minutes_threshold=args.minutes_threshold,
        )
        # New series whenever sender changes vs previous row
        is_new_series = df["sender"].ne(df["sender"].shift())
        # Ensure first row is True
        if len(df) > 0:
            is_new_series.iloc[0] = True
        df["is new message series?"] = is_new_series
        return df

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        messages_by_member = helpers.get_messages(df, member_name, time_period)
        message_series = len(
            messages_by_member[
                (messages_by_member["is new message series?"])
                | (messages_by_member["is conversation starter?"])
            ]
        )
        output_dict[message_series_category].append(message_series)
        output_dict[average_messages_category].append(
            round(helpers.safe_divide(len(messages_by_member), message_series), 2)
        )
        all_messages = helpers.get_messages(df, time_period=time_period)
        total_message_series = len(
            all_messages[
                (all_messages["is new message series?"])
                | (all_messages["is conversation starter?"])
            ]
        )
        output_dict[percent_series_category].append(
            helpers.safe_divide_as_pct(message_series, total_message_series)
        )
