from collections import defaultdict

from src.functions import Function
from src.utils import helpers, constants


class ReactionFlow(Function):
    @staticmethod
    def get_function_name():
        return "reaction_flow"

    @staticmethod
    def get_categories():
        # Uses tableData payload instead of columnar categories
        return []

    @staticmethod
    def get_categories_allowing_graph_total():
        return []

    @staticmethod
    def process_messages_df(df, args):
        return helpers.add_reactions_for_each_message(df)

    def get_table_results(self, result_dict, df, chat_members, args):
        df = self.process_messages_df(df, args)
        reaction_filter = getattr(args, "reaction_type", None)
        if reaction_filter and reaction_filter.lower() == "all":
            reaction_filter = None

        if reaction_filter:
            # Single matrix: reactors on rows, receivers on columns
            result_dict["tableData"] = self._single_matrix(df, reaction_filter, chat_members)
            return df

        # Legacy per-receiver tables
        result_dict["Reactions received by each person"] = []
        for member_name in chat_members:
            helpers.initialize_member(member_name, result_dict)
            self.get_results(result_dict, df, args, member_name=member_name)
        return df

    @staticmethod
    def _single_matrix(df, reaction_filter, chat_members):
        counts = defaultdict(lambda: defaultdict(int))
        for _, row in df.iterrows():
            sender = str(row["sender"])
            for reactor, reaction in row["reactions_per_user"]:
                if (
                    reaction_filter
                    and reaction_filter != "total"
                    and str(reaction) != reaction_filter
                ):
                    continue
                counts[str(reactor)][sender] += 1

        headers = ["Reactor"] + chat_members
        rows = []
        for reactor in chat_members:
            rows.append([reactor] + [counts[reactor].get(receiver, 0) for receiver in chat_members])
        return {
            "headers": headers,
            "rows": rows,
            "meta": {
                "reactionType": reaction_filter or "all",
                "axes": "Reactor rows, Receiver columns",
            },
        }

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        if time_period is not None:
            df = df[df["time_period"] == time_period]
        member_messages = df[df["sender"] == member_name]

        reactions_by_person = defaultdict(lambda: defaultdict(int))
        for _, row in member_messages.iterrows():
            for user, reaction in row["reactions_per_user"]:
                if reaction in constants.REACTION_TYPES:
                    reactions_by_person[user][reaction] += 1
        for user in reactions_by_person:
            total = sum(
                reaction_count for reaction_count in reactions_by_person[user].values()
            )
            reactions_by_person[user]["total"] = total
            for reaction_type in constants.REACTION_TYPES:
                if reaction_type not in reactions_by_person[user]:
                    reactions_by_person[user][reaction_type] = 0
        reactions_by_person = {
            user: reactions_by_person[user]
            for user in sorted(
                reactions_by_person.keys(),
                key=lambda x: reactions_by_person[x]["total"],
                reverse=True,
            )
        }

        columns = ["total"] + constants.REACTION_TYPES

        html_table = '<table border="1">'
        html_table += "<tr>"
        html_table += "<th>Reactor</th>"
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
