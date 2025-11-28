from src.functions import Function
from src.utils import helpers, constants

conversations_participated_in_category = "Conversations participated in"
conversations_participated_in_no_reactions_category = "Conversations participated in (no reactions)"
participation_rate_category = "Participation rate"
participation_rate_no_reactions_category = "Participation rate (no reactions)"


class Participation(Function):
    @staticmethod
    def get_function_name():
        return "participation"

    @staticmethod
    def get_categories():
        return [
            conversations_participated_in_category,
            conversations_participated_in_no_reactions_category,
            participation_rate_category,
            participation_rate_no_reactions_category,
        ]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [conversations_participated_in_category]

    @staticmethod
    def process_messages_df(df, args):
        # Delegate to helper for consistent conversation logic and numbering
        return helpers.compute_conversation_columns(
            df,
            minutes_threshold=args.minutes_threshold,
        )

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

        # Excluding reactions: count only non-reaction messages when determining participation
        nr_messages_by_member = helpers.get_non_reaction_messages(df, member_name, time_period)
        nr_conversations_participated = len(nr_messages_by_member["conversation number"].unique())
        all_nr_messages = helpers.get_non_reaction_messages(df, time_period=time_period)
        total_nr_conversations = len(all_nr_messages["conversation number"].unique())
        output_dict[conversations_participated_in_no_reactions_category].append(
            nr_conversations_participated
        )
        output_dict[participation_rate_no_reactions_category].append(
            helpers.safe_divide_as_pct(
                nr_conversations_participated, total_nr_conversations
            )
        )
