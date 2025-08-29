from src.functions import Function
from src.utils import helpers, constants

conversations_participated_in_category = "Conversations participated in"
participation_rate_category = "Participation rate"


class Participation(Function):
    @staticmethod
    def get_function_name():
        return "participation"

    @staticmethod
    def get_categories():
        return [conversations_participated_in_category, participation_rate_category]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [conversations_participated_in_category]

    @staticmethod
    def process_messages_df(df, args):
        minutes_threshold = args.minutes_threshold or constants.DEFAULT_CONVERSATION_STARTER_THRESHOLD_MINUTES
        seconds = df["time"].diff().dt.total_seconds()
        starters = seconds.gt(minutes_threshold * 60).fillna(True)
        df["is conversation starter?"] = starters
        # Conversation numbers start at 1 and increment on each starter
        df["conversation number"] = starters.cumsum()
        return df

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        messages_by_member = helpers.get_messages(df, member_name, time_period)
        conversations_participated_in = len(
            messages_by_member["conversation number"].unique()
        )
        output_dict[conversations_participated_in_category].append(
            conversations_participated_in
        )
        all_messages = helpers.get_messages(df, time_period=time_period)
        total_conversations = len(all_messages["conversation number"].unique())
        output_dict[participation_rate_category].append(
            helpers.safe_divide_as_pct(
                conversations_participated_in, total_conversations
            )
        )
