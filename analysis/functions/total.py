from analysis.functions import Function
from analysis.utils.constants import GRAPH_TOTAL_KEY
import analysis.utils.helpers as helpers

total_messages_category = "Total messages"
percent_total_messages_category = "Percent of total messages"


class Total(Function):
    @staticmethod
    def get_function_name():
        return "total"

    @staticmethod
    def get_categories():
        return [total_messages_category, percent_total_messages_category]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [total_messages_category]

    def get_results(self, output_dict, df, member_name=None, time_period=None):
        total_messages_by_member = helpers.get_total_messages(
            df, member_name, time_period
        )
        output_dict[total_messages_category].append(total_messages_by_member)
        return total_messages_by_member

    def get_table_results(self, result_dict, df, chat_members, args):
        for member_name in chat_members:
            helpers.initialize_member(member_name, result_dict)
            self.get_results(result_dict, df, member_name)
        total_messages = sum(result_dict[total_messages_category])
        for i in range(len(result_dict[total_messages_category])):
            result_dict[percent_total_messages_category].append(
                round(
                    helpers.safe_divide(
                        result_dict[total_messages_category][i], total_messages
                    )
                    * 100,
                    2,
                )
            )

    def get_graph_results(self, graph_data, df, chat_members, time_periods, args):
        if args.graph_individual:
            self.get_individual_graph_results(
                graph_data, df, chat_members, time_periods
            )
        else:
            self.get_total_graph_results(graph_data, df, time_periods)

    def get_individual_graph_results(self, graph_data, df, chat_members, time_periods):
        for time_period in time_periods:
            total_messages_in_period = 0
            for member_name in chat_members:
                total_messages_in_period += self.get_results(
                    graph_data[member_name], df, member_name, time_period
                )
            for member_name in chat_members:
                graph_data[member_name][percent_total_messages_category].append(
                    round(
                        helpers.safe_divide(
                            graph_data[member_name][total_messages_category][-1],
                            total_messages_in_period,
                        )
                        * 100,
                        2,
                    )
                )

    def get_total_graph_results(self, graph_data, df, time_periods):
        for time_period in time_periods:
            self.get_results(graph_data[GRAPH_TOTAL_KEY], df, None, time_period)
