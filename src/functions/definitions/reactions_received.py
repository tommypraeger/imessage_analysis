from collections import defaultdict

from src.functions import Function
from src.utils import helpers, constants

reactions_given_category = "Reactions given"
reactions_to_others_category = "Reactions to others"


class ReactionsReceived(Function):
    @staticmethod
    def get_function_name():
        return "reactions_received"

    @staticmethod
    def get_categories():
        return [
            "Total messages sent",
            "Total reactions received",
            "Reactions received per message",
        ] + [
            f"{reaction_type} reacts received" for reaction_type in constants.REACTION_TYPES
        ] + [
            f"{reaction_type} reacts received per message" for reaction_type in constants.REACTION_TYPES
        ]
    
    def get_categories_allowing_graph(self):
        return [
            "Total reactions received",
            "Reactions received per message"
        ]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [
            "Total reactions received",
            "Reactions received per message"
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
        output_dict["Total messages sent"].append(total_messages_sent)

        # Calculate the reactions received per message
        reactions_received_per_message = round(
            helpers.safe_divide(total_reactions_received, total_messages_sent),
            2
        )

        # Calculate reactions by each person
        reactions_by_person = defaultdict(lambda: defaultdict(int))
        for _, row in df.iterrows():
            for user, reaction in row["reactions_per_user"]:
                if reaction in constants.REACTION_TYPES:
                    reactions_by_person[user][reaction] += 1

        # Update the output_dict with the calculated values
        output_dict["Total reactions received"].append(total_reactions_received)
        output_dict["Reactions received per message"].append(reactions_received_per_message)

        # Reaction types stats: Like, Love, Laugh, etc.
        for reaction_type in constants.REACTION_TYPES:
            total_reacts = sum(
                count for user_reactions in reactions_by_person.values()
                for react_type, count in user_reactions.items()
                if react_type == reaction_type
            )
            output_dict[f"{reaction_type} reacts received"].append(total_reacts)
            output_dict[f"{reaction_type} reacts received per message"].append(
                round(
                    helpers.safe_divide(total_reacts, total_messages_sent),
                    4
                )
            )
