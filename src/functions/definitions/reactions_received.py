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
        # Filter messages that belong to the specified member (if time_period is provided)
        if time_period is not None:
            df = df[df["time_period"] == time_period]
        if member_name is not None:
            df = df[df["sender"] == member_name]

        # Calculate the total reactions received by the member
        total_reactions_received = int(df["reaction_count"].sum())

        # Calculate the number of messages sent by the member
        total_messages_sent = len(df)
        output_dict[total_messages_sent_category].append(total_messages_sent)

        # Calculate the reactions received per message
        reactions_received_per_message = round(
            helpers.safe_divide(total_reactions_received, total_messages_sent),
            4
        )

        # Calculate reactions by each person
        reactions_by_person = defaultdict(lambda: defaultdict(int))
        for _, row in df.iterrows():
            for user, reaction in row["reactions_per_user"]:
                if reaction in constants.REACTION_TYPES:
                    reactions_by_person[user][reaction] += 1

        # Update the output_dict with the calculated values
        output_dict[total_reactions_received_category].append(total_reactions_received)
        output_dict[reactions_received_per_message_category].append(reactions_received_per_message)

        # Reaction types stats: Like, Love, Laugh, etc.
        for reaction_type in constants.REACTION_TYPES:
            total_reacts = sum(
                count
                for user_reactions in reactions_by_person.values()
                for react_type, count in user_reactions.items()
                if react_type == reaction_type
            )
            rt_title = reaction_type.title()
            output_dict[f"{rt_title} reacts received"].append(total_reacts)
            output_dict[f"{rt_title} reacts received per message"].append(
                round(
                    helpers.safe_divide(total_reacts, total_messages_sent),
                    4
                )
            )
