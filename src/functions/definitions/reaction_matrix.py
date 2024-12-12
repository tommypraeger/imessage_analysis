from collections import defaultdict

from src.functions import Function
from src.utils import helpers, constants


class ReactionMatrix(Function):
    @staticmethod
    def get_function_name():
        return "reaction_matrix"

    @staticmethod
    def get_categories():
        return [
            "Reactions received by each person",
        ] 
    
    def get_categories_allowing_graph(self):
        return []

    @staticmethod
    def get_categories_allowing_graph_total():
        return []
    
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
        member_messages = df[df["sender"] == member_name]

        # Calculate reactions by each person
        reactions_by_person = defaultdict(lambda: defaultdict(int))
        for _, row in member_messages.iterrows():
            for user, reaction in row["reactions_per_user"]:
                if reaction in constants.REACTION_TYPES:
                    reactions_by_person[user][reaction] += 1
        for user in reactions_by_person:
            total = sum(reaction_count for reaction_count in reactions_by_person[user].values())
            reactions_by_person[user]["total"] = total
            for reaction_type in constants.REACTION_TYPES:
                if reaction_type not in reactions_by_person[user]:
                    reactions_by_person[user][reaction_type] = 0
        reactions_by_person = {
            user: reactions_by_person[user]
            for user in sorted(reactions_by_person.keys(), key=lambda x: reactions_by_person[x]["total"], reverse=True)
        }

        # Columns order
        columns = ["total", "love", "like", "dislike", "laugh", "emphasize", "question", "custom emoji"]

        # Generate HTML
        html_table = "<table border=\"1\">"
        html_table += "<tr>"
        html_table += "<th>Name</th>"
        for column in columns:
            html_table += f"<th>{column.capitalize()}</th>"
        html_table += "</tr>"

        for name, reactions in reactions_by_person.items():
            html_table += "<tr>"
            html_table += f"<td>{name}</td>"
            for column in columns:
                html_table += f"<td>{reactions.get(column, 0)}</td>"
            html_table += "</tr>"

        html_table += "</table>"

        output_dict["Reactions received by each person"].append(html_table)
