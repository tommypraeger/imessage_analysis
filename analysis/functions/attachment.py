from analysis.functions import Function
from analysis.utils.constants import GRAPH_TOTAL_KEY
import analysis.utils.helpers as helpers

attachment_category = "Messages that are attachments"
percent_attachment_category = "Percent of messages that are attachments"


class Attachment(Function):
    @staticmethod
    def get_function_name():
        return "attachment"

    @staticmethod
    def get_categories():
        return [attachment_category, percent_attachment_category]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [attachment_category, percent_attachment_category]

    def process_df(df):
        df["is attachment?"] = df["type"].apply(helpers.is_attachment)

    def get_results(self, output_dict, df, member_name=None, time_period=None):
        nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
        attachment_messages = len(nr_messages[nr_messages["is attachment?"]])
        output_dict[attachment_category].append(attachment_messages)
        output_dict[percent_attachment_category].append(
            round(helpers.safe_divide(attachment_messages, len(nr_messages)) * 100, 2)
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
