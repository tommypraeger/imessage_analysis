from src.functions import Function
from src.utils import helpers, constants


message_series_category = "Total number of message series"
average_messages_category = "Average messages per series"
percent_series_category = "Percent of total message series"


def add_message_series_columns(df, minutes_threshold=None):
    """Annotate df with conversation and message-series markers."""
    df = helpers.compute_conversation_columns(df, minutes_threshold=minutes_threshold)
    is_new_series = df["sender"].ne(df["sender"].shift())
    if len(df) > 0:
        is_new_series.iloc[0] = True
    df["is new message series?"] = is_new_series
    return df


def message_series_count_by_sender(df, member_name=None, time_period=None):
    """Count message series per sender, matching MessageSeries semantics (non-reactions only)."""
    msgs = helpers.get_non_reaction_messages(df, member_name, time_period)
    if "is new message series?" not in msgs.columns:
        msgs = add_message_series_columns(msgs)
    series_mask = msgs["is new message series?"].fillna(False)
    starter_mask = msgs.get("is conversation starter?", False)
    combined = series_mask | starter_mask
    return msgs[combined].groupby("sender").size().to_dict()


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
        return add_message_series_columns(df, minutes_threshold=args.minutes_threshold)

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        messages_by_member = helpers.get_non_reaction_messages(df, member_name, time_period)
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
        all_messages = helpers.get_non_reaction_messages(df, time_period=time_period)
        total_message_series = len(
            all_messages[
                (all_messages["is new message series?"])
                | (all_messages["is conversation starter?"])
            ]
        )
        output_dict[percent_series_category].append(
            helpers.safe_divide_as_pct(message_series, total_message_series)
        )
