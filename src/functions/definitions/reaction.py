from src.functions import Function
from src.utils import helpers, constants

reactions_messages_category = "Reaction messages (including removing reactions)"
percent_all_reactions_category = "Percent of all reactions messages"
percent_reactions_category = "Percent of messages that are reactions"
removed_reactions = "Removed reactions"

# TODO: accept reaction list as arg (implemented on frontend for now)


class Reaction(Function):
    @staticmethod
    def get_function_name():
        return "reaction"

    @staticmethod
    def get_categories():
        categories = [
            reactions_messages_category,
            percent_all_reactions_category,
            percent_reactions_category,
            removed_reactions,
        ]
        for rt in constants.REACTION_TYPES:
            categories.append(f"{rt.title()} reacts")
            categories.append(f"Percent of reactions that are {rt.title()} reacts")
        return categories

    @staticmethod
    def get_categories_allowing_graph_total():
        categories = [
            reactions_messages_category,
            percent_reactions_category,
            removed_reactions,
        ]
        for rt in constants.REACTION_TYPES:
            categories.append(f"{rt.title()} reacts")
            categories.append(f"Percent of reactions that are {rt.title()} reacts")
        return categories

    @staticmethod
    def process_messages_df(df, args):
        mt = df["message_type"].astype("string")
        df["is removed reaction?"] = mt.str.startswith("removed", na=False)
        return df

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        messages = helpers.get_messages(df, member_name, time_period)
        mt_series = messages["message_type"].astype("string")
        is_reaction = mt_series.isin(constants.REACTION_TYPES)
        reaction_messages_by_member = int(is_reaction.sum())
        output_dict[reactions_messages_category].append(reaction_messages_by_member)
        # Percent of this member's messages that are reactions
        total_messages_by_member = helpers.get_total_messages(df, member_name, time_period)
        output_dict[percent_reactions_category].append(
            helpers.safe_divide_as_pct(
                reaction_messages_by_member, total_messages_by_member
            )
        )

        # Percent of all reaction messages that belong to this member
        all_messages = helpers.get_messages(df, time_period=time_period)
        total_reaction_messages = int(
            all_messages["message_type"].astype("string").isin(constants.REACTION_TYPES).sum()
        )
        output_dict[percent_all_reactions_category].append(
            helpers.safe_divide_as_pct(
                reaction_messages_by_member,
                total_reaction_messages,
            )
        )

        reactions = reaction_messages_by_member
        removed_reacts = int(messages["is removed reaction?"].sum())

        # Count per reaction type (vectorized)
        per_type_counts = {rt: int((mt_series == rt).sum()) for rt in constants.REACTION_TYPES}

        output_dict[removed_reactions].append(removed_reacts)

        for rt in constants.REACTION_TYPES:
            count_label = f"{rt.title()} reacts"
            percent_label = f"Percent of reactions that are {rt.title()} reacts"
            count = per_type_counts[rt]
            output_dict[count_label].append(count)
            output_dict[percent_label].append(
                helpers.safe_divide_as_pct(count, reactions)
            )
