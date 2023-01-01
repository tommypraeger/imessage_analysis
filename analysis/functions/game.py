from analysis.functions import Function
from analysis.utils.constants import GRAPH_TOTAL_KEY
import analysis.utils.helpers as helpers

games_category = "Messages that are games"
percent_games_category = "Percent of messages that are games"
game_starts_category = "Messages that start games"
percent_game_starts_category = "Percent of games started"


class Game(Function):
    @staticmethod
    def get_function_name():
        return "game"

    @staticmethod
    def get_categories():
        return [
            games_category,
            percent_games_category,
            game_starts_category,
            percent_game_starts_category,
        ]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [games_category, percent_games_category, game_starts_category]

    def process_df(self, df):
        df["is game message?"] = df.apply(
            lambda msg: helpers.is_game_message(msg.text, msg.type), axis=1
        )
        df["is game start?"] = df.apply(
            lambda msg: helpers.is_game_start(msg.text, msg.type), axis=1
        )

    def get_results(self, output_dict, df, member_name=None, time_period=None):
        nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
        game_messages = len(nr_messages[nr_messages["is game message?"]])
        game_starts = len(nr_messages[nr_messages["is game start?"]])
        output_dict[games_category].append(game_messages)
        output_dict[percent_games_category].append(
            round(helpers.safe_divide(game_messages, len(nr_messages)) * 100, 2)
        )
        output_dict[game_starts_category].append(game_starts)
        return game_starts

    def get_table_results(self, result_dict, df, chat_members, args):
        self.process_df(df)
        for member_name in chat_members:
            helpers.initialize_member(member_name, result_dict)
            self.get_results(result_dict, df, member_name)
        total_game_starts = sum(result_dict[game_starts_category])
        for i in range(len(result_dict[game_starts_category])):
            result_dict[percent_game_starts_category].append(
                round(
                    helpers.safe_divide(
                        result_dict[game_starts_category][i], total_game_starts
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
            total_games_started_in_period = 0
            for member_name in chat_members:
                total_games_started_in_period += self.get_results(
                    graph_data[member_name], df, member_name, time_period
                )
            for member_name in chat_members:
                graph_data[member_name][percent_game_starts_category].append(
                    round(
                        helpers.safe_divide(
                            graph_data[member_name][game_starts_category][-1],
                            total_games_started_in_period,
                        )
                        * 100,
                        2,
                    )
                )

    def get_total_graph_results(self, graph_data, df, time_periods):
        for time_period in time_periods:
            self.get_results(graph_data[GRAPH_TOTAL_KEY], df, None, time_period)
