from collections import defaultdict

from src.functions import Function
from src.utils import helpers, constants

total_messages_sent_category = "Total messages sent"
total_reactions_received_category = "Total reactions received"
reactions_received_per_message_category = "Reactions received per message"


class ReactionsReceived(Function):
    @staticmethod
    def get_function_name():
        return "reactions_received"

    @staticmethod
    def get_categories():
        base = [
            total_messages_sent_category,
            total_reactions_received_category,
            reactions_received_per_message_category,
        ]
        per_type = []
        for reaction_type in constants.REACTION_TYPES:
            rt_title = reaction_type.title()
            per_type.append(f"{rt_title} reacts received")
            per_type.append(f"{rt_title} reacts received per message")
        return base + per_type
    
    def get_categories_allowing_graph(self):
        return [
            total_reactions_received_category,
            reactions_received_per_message_category,
        ]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [
            total_reactions_received_category,
            reactions_received_per_message_category,
        ]
    
    @staticmethod
    def process_messages_df(df, args):
        """
        Process the dataframe to calculate necessary columns such as total reactions and reaction stats.
        """
        return helpers.add_reactions_for_each_message(df)
    
    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        """
        Fill in results from analysis into the output dictionary using the processed dataframe.
        """
        # Filter messages that belong to the specified member and/or time period
        if time_period is not None:
            df = df[df["time_period"] == time_period]
        if member_name is not None:
            df = df[df["sender"] == member_name]

        # Totals
        total_messages_sent = len(df)
        total_reactions_received = int(df["reaction_count"].sum())
        reactions_received_per_message = round(
            helpers.safe_divide(total_reactions_received, total_messages_sent), 4
        )

        output_dict[total_messages_sent_category].append(total_messages_sent)
        output_dict[total_reactions_received_category].append(total_reactions_received)
        output_dict[reactions_received_per_message_category].append(
            reactions_received_per_message
        )

        # Per-type counts (reactor identity not needed here)
        long = df[["reactions_per_user"]].explode("reactions_per_user")
        if len(long) and "reactions_per_user" in long:
            long = long.dropna(subset=["reactions_per_user"])  # drop messages with no reactions
            if len(long):
                # Extract reaction_type from tuple (user, reaction_type)
                long["reaction_type"] = long["reactions_per_user"].str[1]
                per_type_counts = long["reaction_type"].value_counts()
            else:
                per_type_counts = {}
        else:
            per_type_counts = {}

        for reaction_type in constants.REACTION_TYPES:
            total_reacts = int(per_type_counts.get(reaction_type, 0))
            rt_title = reaction_type.title()
            output_dict[f"{rt_title} reacts received"].append(total_reacts)
            output_dict[f"{rt_title} reacts received per message"].append(
                round(helpers.safe_divide(total_reacts, total_messages_sent), 4)
            )
