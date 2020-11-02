from analysis.utils.initialize_result_dict import initialize_result_dict
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers

def main(result_dict, df, chat_members):
    result_dict['messages that contain emojis'] = []
    result_dict['% of messages that include emojis'] = []
    df['includes emoji?'] = df['text'].apply(helpers.includes_emoji)
    for member_name in chat_members:
        total_messages, non_reaction_messages = initialize_result_dict(member_name, df, result_dict)
        if total_messages > 0:
            emoji_messages = len(
                df[(df['includes emoji?']) & (df['sender'] == member_name)]
            )
            result_dict['messages that contain emojis'].append(emoji_messages)
            result_dict['% of messages that include emojis'].append(
                round((emoji_messages / non_reaction_messages) * 100, 2)
            )
