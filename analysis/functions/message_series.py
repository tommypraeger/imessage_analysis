from analysis.functions import Function
import analysis.utils.helpers as helpers


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
        return [message_series_category, average_messages_category]

    @staticmethod
    def process_messages_df(df, args):
        minutes_threshold = args.minutes_threshold
        df["is conversation starter?"] = (
            df["time"]
            .diff()
            .apply(
                lambda diff: helpers.is_conversation_starter(diff, minutes_threshold)
            )
        )
        df.iloc[0, df.columns.get_loc("is conversation starter?")] = True
        df["is new message series?"] = df["sender"].apply(lambda x: True)
        df["is new message series?"] = (
            df["is new message series?"]
            .shift()
            .where(df["sender"].shift() != df["sender"], False)
        )
        df.iloc[0, df.columns.get_loc("is new message series?")] = True

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        messages_by_member = helpers.get_non_reaction_messages(
            df, member_name, time_period
        )
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
