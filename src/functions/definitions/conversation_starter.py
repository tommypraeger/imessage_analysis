from src.functions import Function
from src.utils import helpers, constants

conversations_started_category = "Conversations started"
percent_started_category = "Percent of conversations started"


class ConversationStarter(Function):
    @staticmethod
    def get_function_name():
        return "conversation_starter"

    @staticmethod
    def get_categories():
        return [conversations_started_category, percent_started_category]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [conversations_started_category]

    @staticmethod
    def process_messages_df(df, args):
        # Use global helper to ensure reactions never start conversations and
        # reactions inherit the parent's conversation.
        return helpers.compute_conversation_columns(
            df,
            minutes_threshold=args.minutes_threshold,
        )

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        messages_by_member = helpers.get_messages(df, member_name, time_period)
        conversation_starters = len(
            messages_by_member[messages_by_member["is conversation starter?"]]
        )
        output_dict[conversations_started_category].append(conversation_starters)
        all_messages = helpers.get_messages(df, time_period=time_period)
        total_conversation_starters = len(
            all_messages[all_messages["is conversation starter?"]]
        )
        output_dict[percent_started_category].append(
            helpers.safe_divide_as_pct(
                conversation_starters, total_conversation_starters
            )
        )
