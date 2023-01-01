from analysis.functions import Function
from analysis.utils.constants import GRAPH_TOTAL_KEY
import analysis.utils.helpers as helpers

conversations_started_category = "Conversations started"
percent_started_category = "Percent of conversations started"


class ConversationStarter(Function):
    @staticmethod
    def get_function_name():
        return "conversation_starter"

    @staticmethod
    def get_categories():
        return [conversations_started_category, percent_started_category]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [conversations_started_category]

    def process_df(self, df, minutes_threshold):
        df["is conversation starter?"] = (
            df["time"]
            .diff()
            .apply(
                lambda diff: helpers.is_conversation_starter(diff, minutes_threshold)
            )
        )
        df.iloc[0, df.columns.get_loc("is conversation starter?")] = True

    def get_results(self, output_dict, df, member_name=None, time_period=None):
        nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
        conversation_starters = len(
            nr_messages[nr_messages["is conversation starter?"]]
        )
        output_dict[conversations_started_category].append(conversation_starters)
        return conversation_starters

    def get_table_results(self, result_dict, df, chat_members, args):
        self.process_df(df, args.minutes_threshold)
        for member_name in chat_members:
            helpers.initialize_member(member_name, result_dict)
            self.get_results(result_dict, df, member_name)
        total_conversation_starters = sum(result_dict[conversations_started_category])
        for i in range(len(result_dict[conversations_started_category])):
            result_dict[percent_started_category].append(
                round(
                    helpers.safe_divide(
                        result_dict[conversations_started_category][i],
                        total_conversation_starters,
                    )
                    * 100,
                    2,
                )
            )

    def get_graph_results(self, graph_data, df, chat_members, time_periods, args):
        self.process_df(df, args.minutes_threshold)
        if args.graph_individual:
            self.get_individual_graph_results(
                graph_data, df, chat_members, time_periods
            )
        else:
            self.get_total_graph_results(graph_data, df, time_periods)

    def get_individual_graph_results(self, graph_data, df, chat_members, time_periods):
        for time_period in time_periods:
            total_conversations_started_in_period = 0
            for member_name in chat_members:
                total_conversations_started_in_period += self.get_results(
                    graph_data[member_name], df, member_name, time_period
                )
            for member_name in chat_members:
                graph_data[member_name][percent_started_category].append(
                    round(
                        helpers.safe_divide(
                            graph_data[member_name][conversations_started_category][-1],
                            total_conversations_started_in_period,
                        )
                        * 100,
                        2,
                    )
                )

    def get_total_graph_results(self, graph_data, df, time_periods):
        for time_period in time_periods:
            self.get_results(graph_data[GRAPH_TOTAL_KEY], df, None, time_period)
