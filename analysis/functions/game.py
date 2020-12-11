from analysis.utils.initialize_result_dict import initialize_result_dict
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers


def main(result_dict, df, chat_members):
    result_dict['messages that are games'] = []
    result_dict['% of messages that are games'] = []
    result_dict['messages that are game starts'] = []
    result_dict['% of messages that are game starts'] = []
    df['is game message?'] = df.apply(
        lambda msg: helpers.is_game_message(msg.text, msg.type), axis=1)
    df['is game start?'] = df.apply(lambda msg: helpers.is_game_start(msg.text, msg.type), axis=1)
    for member_name in chat_members:
        _, non_reaction_messages = initialize_result_dict(member_name, df, result_dict)
        game_messages = len(
            df[(df['is game message?']) & (df['sender'] == member_name)]
        )
        game_starts = len(
            df[(df['is game start?']) & (df['sender'] == member_name)]
        )
        result_dict['messages that are games'].append(game_messages)
        result_dict['% of messages that are games'].append(
            round(helpers.safe_divide(game_messages, non_reaction_messages) * 100, 2)
        )
        result_dict['messages that are game starts'].append(game_starts)
        result_dict['% of messages that are game starts'].append(
            round(helpers.safe_divide(game_starts, non_reaction_messages) * 100, 2)
        )
