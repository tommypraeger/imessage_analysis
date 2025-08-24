from src.functions import Function
from src.utils import helpers, constants

total_messages_category = "Total messages"
non_reaction_messages_category = "Messages that are not reactions"
percent_all_non_reaction_category = "Percent of all messages that are not reactions"
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
            total_messages_category,
            non_reaction_messages_category,
            percent_all_non_reaction_category,
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
            total_messages_category,
            non_reaction_messages_category,
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
        df["is removed reaction?"] = df["message_type"].apply(
            helpers.is_removed_reaction
        )
        return df

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        total_messages_by_member = helpers.get_total_messages(
            df, member_name, time_period
        )
        nr_messages_by_member = helpers.get_total_non_reaction_messages(
            df, member_name, time_period
        )
        output_dict[total_messages_category].append(total_messages_by_member)
        reaction_messages_by_member = total_messages_by_member - nr_messages_by_member
        output_dict[reactions_messages_category].append(reaction_messages_by_member)
        output_dict[non_reaction_messages_category].append(nr_messages_by_member)
        output_dict[percent_reactions_category].append(
            helpers.safe_divide_as_pct(
                reaction_messages_by_member, total_messages_by_member
            )
        )

        total_messages = helpers.get_total_messages(df, time_period=time_period)
        total_non_reaction_messages = helpers.get_total_non_reaction_messages(
            df, time_period=time_period
        )
        total_reaction_messages = total_messages - total_non_reaction_messages
        output_dict[percent_all_reactions_category].append(
            helpers.safe_divide_as_pct(
                reaction_messages_by_member,
                total_reaction_messages,
            )
        )

        output_dict[percent_all_non_reaction_category].append(
            helpers.safe_divide_as_pct(
                nr_messages_by_member,
                total_non_reaction_messages,
            )
        )

        messages = helpers.get_messages(df, member_name, time_period)
        reactions = len(messages[messages["message_type"].apply(helpers.is_reaction)])
        removed_reacts = len(messages[messages["is removed reaction?"]])

        # Count per reaction type
        per_type_counts = {rt: len(messages[messages.message_type == rt]) for rt in constants.REACTION_TYPES}

        output_dict[removed_reactions].append(removed_reacts)

        for rt in constants.REACTION_TYPES:
            count_label = f"{rt.title()} reacts"
            percent_label = f"Percent of reactions that are {rt.title()} reacts"
            count = per_type_counts[rt]
            output_dict[count_label].append(count)
            output_dict[percent_label].append(
                helpers.safe_divide_as_pct(count, reactions)
            )
