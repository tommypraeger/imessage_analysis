from analysis.functions import Function
import analysis.utils.helpers as helpers

total_messages_category = "Total messages"
non_reaction_messages_category = "Messages that are not reactions"
percent_all_non_reaction_category = "Percent of all messages that are not reactions"
reactions_messages_category = "Reaction messages (including removing reactions)"
percent_all_reactions_category = "Percent of all reactions messages"
percent_reactions_category = "Percent of messages that are reactions"
reactions_category = "Reactions (not including removed reactions)"
likes_category = "Like reacts"
percent_likes_category = "Percent of reactions that are like reacts"
loves_category = "Love reacts"
percent_loves_category = "Percent of reactions that are love reacts"
dislikes_category = "Dislike reacts"
percent_dislikes_category = "Percent of reactions that are dislike reacts"
laughs_category = "Laugh reacts"
percent_laugh_category = "Percent of reactions that are laugh reacts"
emphasis_category = "Emphasis reacts"
percent_emphasis_category = "Percent of reactions that are emphasis reacts"
questions_category = "Question reacts"
percent_questions_category = "Percent of reactions that are question reacts"


class Reaction(Function):
    @staticmethod
    def get_function_name():
        return "reaction"

    @staticmethod
    def get_categories():
        return [
            total_messages_category,
            non_reaction_messages_category,
            percent_all_non_reaction_category,
            reactions_messages_category,
            percent_all_reactions_category,
            percent_reactions_category,
            reactions_category,
            likes_category,
            percent_likes_category,
            loves_category,
            percent_loves_category,
            dislikes_category,
            percent_dislikes_category,
            laughs_category,
            percent_laugh_category,
            emphasis_category,
            percent_emphasis_category,
            questions_category,
            percent_questions_category,
        ]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [
            total_messages_category,
            non_reaction_messages_category,
            reactions_messages_category,
            percent_reactions_category,
            reactions_category,
            likes_category,
            percent_likes_category,
            loves_category,
            percent_loves_category,
            dislikes_category,
            percent_dislikes_category,
            laughs_category,
            percent_laugh_category,
            emphasis_category,
            percent_emphasis_category,
            questions_category,
            percent_questions_category,
        ]

    @staticmethod
    def process_messages_df(df, args):
        df["reaction action"] = df["text"].apply(helpers.reaction_action)
        df["like react action"] = df["text"].apply(helpers.like_react_action)
        df["love react action"] = df["text"].apply(helpers.love_react_action)
        df["dislike react action"] = df["text"].apply(helpers.dislike_react_action)
        df["laugh react action"] = df["text"].apply(helpers.laugh_react_action)
        df["emphasis react action"] = df["text"].apply(helpers.emphasis_react_action)
        df["question react action"] = df["text"].apply(helpers.question_react_action)

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

        total_messages = helpers.get_total_messages(time_period=time_period)
        total_non_reaction_messages = helpers.get_total_non_reaction_messages(
            time_period=time_period
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
        reactions = int(messages["reaction action"].sum())
        like_reacts = int(messages["like react action"].sum())
        love_reacts = int(messages["love react action"].sum())
        dislike_reacts = int(messages["dislike react action"].sum())
        laugh_reacts = int(messages["laugh react action"].sum())
        emphasis_reacts = int(messages["emphasis react action"].sum())
        question_reacts = int(messages["question react action"].sum())

        output_dict[reactions_category].append(reactions)

        output_dict[likes_category].append(like_reacts)
        output_dict[percent_likes_category].append(
            helpers.safe_divideas_pct(like_reacts, reactions)
        )

        output_dict[loves_category].append(love_reacts)
        output_dict[percent_loves_category].append(
            helpers.safe_divideas_pct(love_reacts, reactions)
        )

        output_dict[dislikes_category].append(dislike_reacts)
        output_dict[percent_dislikes_category].append(
            helpers.safe_divideas_pct(dislike_reacts, reactions)
        )

        output_dict[laughs_category].append(laugh_reacts)
        output_dict[percent_laugh_category].append(
            helpers.safe_divideas_pct(laugh_reacts, reactions)
        )

        output_dict[emphasis_category].append(emphasis_reacts)
        output_dict[percent_emphasis_category].append(
            helpers.safe_divideas_pct(emphasis_reacts, reactions)
        )

        output_dict[questions_category].append(question_reacts)
        output_dict[percent_questions_category].append(
            helpers.safe_divideas_pct(question_reacts, reactions)
        )
