from src.functions import Function
from src.utils import helpers

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

    @staticmethod
    def process_messages_df(df, args):
        mt = df["message_type"].astype("string")
        df["is game message?"] = mt.isin(["game", "game start"])
        df["is game start?"] = mt.eq("game start")
        return df

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
        game_messages = len(nr_messages[nr_messages["is game message?"]])
        game_starts = len(nr_messages[nr_messages["is game start?"]])
        output_dict[games_category].append(game_messages)
        output_dict[percent_games_category].append(
            helpers.safe_divide_as_pct(game_messages, len(nr_messages))
        )
        output_dict[game_starts_category].append(game_starts)
        all_messages = helpers.get_non_reaction_messages(df, time_period=time_period)
        total_game_starts = len(all_messages[all_messages["is game start?"]])
        output_dict[percent_game_starts_category].append(
            helpers.safe_divide_as_pct(game_starts, total_game_starts)
        )
