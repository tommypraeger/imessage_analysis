from analysis.functions import Function
from analysis.utils.constants import GRAPH_TOTAL_KEY
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

    def process_df(self, df):
        df["reaction action"] = df["text"].apply(helpers.reaction_action)
        df["like react action"] = df["text"].apply(helpers.like_react_action)
        df["love react action"] = df["text"].apply(helpers.love_react_action)
        df["dislike react action"] = df["text"].apply(helpers.dislike_react_action)
        df["laugh react action"] = df["text"].apply(helpers.laugh_react_action)
        df["emphasis react action"] = df["text"].apply(helpers.emphasis_react_action)
        df["question react action"] = df["text"].apply(helpers.question_react_action)

    def get_results(self, output_dict, df, member_name=None, time_period=None):
        total_messages = helpers.get_total_messages(df, member_name, time_period)
        nr_messages = helpers.get_total_non_reaction_messages(
            df, member_name, time_period
        )
        output_dict[total_messages_category].append(total_messages)
        reaction_messages = total_messages - nr_messages
        output_dict[reactions_messages_category].append(reaction_messages)
        output_dict[non_reaction_messages_category].append(nr_messages)
        output_dict[percent_reactions_category].append(
            round((1 - helpers.safe_divide(nr_messages, total_messages)) * 100, 2)
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
            round(helpers.safe_divide(like_reacts, reactions) * 100, 2)
        )

        output_dict[loves_category].append(love_reacts)
        output_dict[percent_loves_category].append(
            round(helpers.safe_divide(love_reacts, reactions) * 100, 2)
        )

        output_dict[dislikes_category].append(dislike_reacts)
        output_dict[percent_dislikes_category].append(
            round(helpers.safe_divide(dislike_reacts, reactions) * 100, 2)
        )

        output_dict[laughs_category].append(laugh_reacts)
        output_dict[percent_laugh_category].append(
            round(helpers.safe_divide(laugh_reacts, reactions) * 100, 2)
        )

        output_dict[emphasis_category].append(emphasis_reacts)
        output_dict[percent_emphasis_category].append(
            round(helpers.safe_divide(emphasis_reacts, reactions) * 100, 2)
        )

        output_dict[questions_category].append(question_reacts)
        output_dict[percent_questions_category].append(
            round(helpers.safe_divide(question_reacts, reactions) * 100, 2)
        )

        return reaction_messages, nr_messages

    def get_table_results(self, result_dict, df, chat_members, args):
        self.process_df(df)
        for member_name in chat_members:
            helpers.initialize_member(member_name, result_dict)
            self.get_results(result_dict, df, member_name)
        total_reaction_messages = sum(result_dict[reactions_messages_category])
        total_non_reaction_messages = sum(result_dict[non_reaction_messages_category])
        for i in range(len(result_dict[total_messages_category])):
            result_dict[percent_all_reactions_category].append(
                round(
                    helpers.safe_divide(
                        result_dict[reactions_messages_category][i],
                        total_reaction_messages,
                    )
                    * 100,
                    2,
                )
            )
            result_dict[percent_all_non_reaction_category].append(
                round(
                    helpers.safe_divide(
                        result_dict[non_reaction_messages_category][i],
                        total_non_reaction_messages,
                    )
                    * 100,
                    2,
                )
            )

    def get_graph_results(self, graph_data, df, chat_members, time_periods, args):
        self.process_df(df)
        if args.graph_individual:
            self.get_individual_graph_results(
                graph_data, df, chat_members, time_periods
            )
        else:
            self.get_total_graph_results(graph_data, df, time_periods)

    def get_individual_graph_results(self, graph_data, df, chat_members, time_periods):
        for time_period in time_periods:
            total_reaction_messages_in_period = 0
            total_non_reaction_messages_in_period = 0
            for member_name in chat_members:
                (
                    member_reaction_messages_in_period,
                    member_nr_messages_in_period,
                ) = self.get_results(
                    graph_data[member_name], df, member_name, time_period
                )
                total_reaction_messages_in_period += member_reaction_messages_in_period
                total_non_reaction_messages_in_period += member_nr_messages_in_period
            for member_name in chat_members:
                graph_data[member_name][percent_all_reactions_category].append(
                    round(
                        helpers.safe_divide(
                            graph_data[member_name][reactions_messages_category][-1],
                            total_reaction_messages_in_period,
                        )
                        * 100,
                        2,
                    )
                )
                graph_data[member_name][percent_all_non_reaction_category].append(
                    round(
                        helpers.safe_divide(
                            graph_data[member_name][non_reaction_messages_category][-1],
                            total_non_reaction_messages_in_period,
                        )
                        * 100,
                        2,
                    )
                )

    def get_total_graph_results(self, graph_data, df, time_periods):
        for time_period in time_periods:
            self.get_results(graph_data[GRAPH_TOTAL_KEY], df, None, time_period)
