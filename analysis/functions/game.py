import analysis.utils.constants as constants
import analysis.utils.helpers as helpers


def main(result_dict, df, chat_members):
    result_dict['messages that are games'] = []
    result_dict['% of messages that are games'] = []
    result_dict['messages that are game starts'] = []
    result_dict['% of game starts that are by this person'] = []
    df['is game message?'] = df.apply(
        lambda msg: helpers.is_game_message(msg.text, msg.type), axis=1)
    df['is game start?'] = df.apply(lambda msg: helpers.is_game_start(msg.text, msg.type), axis=1)
    for member_name in chat_members:
        helpers.initialize_member(member_name, result_dict)
        non_reaction_messages = helpers.get_total_non_reaction_messages(df, member_name)
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
    total_game_starts = sum(result_dict['messages that are game starts'])
    for i in range(len(result_dict['messages that are game starts'])):
        result_dict['% of game starts that are by this person'].append(
            round(
                helpers.safe_divide(
                    result_dict['messages that are game starts'][i], total_game_starts
                ) * 100,
                2
            )
        )
