from src.functions import Function
from src.utils import helpers

games_category = "Messages that are games"
percent_games_category = "Percent of messages that are games"


class Game(Function):
    @staticmethod
    def get_function_name():
        return "game"

    @staticmethod
    def get_categories():
        return [
            games_category,
            percent_games_category,
        ]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [games_category, percent_games_category]

    @staticmethod
    def process_messages_df(df, args):
        df["is game message?"] = df.apply(
            lambda msg: helpers.is_game_message(msg.text, msg.type), axis=1
        )

    @staticmethod
    def get_results(output_dict, df, args, member_name=None, time_period=None):
        nr_messages = helpers.get_non_reaction_messages(df, member_name, time_period)
        game_messages = len(nr_messages[nr_messages["is game message?"]])
        output_dict[games_category].append(game_messages)
        output_dict[percent_games_category].append(
            helpers.safe_divide_as_pct(game_messages, len(nr_messages))
        )
