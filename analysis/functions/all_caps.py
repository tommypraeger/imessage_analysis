from analysis.functions import Function
from analysis.utils.constants import GRAPH_TOTAL_KEY
from analysis.utils import helpers

all_caps_category = "Messages in all caps"
percent_all_caps_category = "Percent of messages that are in all caps"


class AllCaps(Function):
    @staticmethod
    def get_function_name():
        return "all_caps"

    @staticmethod
    def get_categories():
        return [all_caps_category, percent_all_caps_category]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [all_caps_category, percent_all_caps_category]

    def process_df(self, df):
        df["is all caps?"] = df["text"].apply(helpers.is_all_caps)

    def get_results(self, output_dict, df, member_name=None, time_period=None):
        nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
        all_caps_messages = len(nr_messages[nr_messages["is all caps?"]])
        output_dict[all_caps_category].append(all_caps_messages)
        output_dict[percent_all_caps_category].append(
            round(helpers.safe_divide(all_caps_messages, len(nr_messages)) * 100, 2)
        )

    def get_table_results(self, result_dict, df, chat_members, args):
        self.process_df(df)
        for member_name in chat_members:
            helpers.initialize_member(member_name, result_dict)
            self.get_results(result_dict, df, member_name)

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
            for member_name in chat_members:
                self.get_results(graph_data[member_name], df, member_name, time_period)

    def get_total_graph_results(self, graph_data, df, time_periods):
        for time_period in time_periods:
            self.get_results(graph_data[GRAPH_TOTAL_KEY], df, None, time_period)
