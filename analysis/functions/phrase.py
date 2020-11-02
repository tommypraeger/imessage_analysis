from analysis.utils.initialize_result_dict import initialize_result_dict
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers

def main(result_dict, df, chat_members, phrase, case_sensitive, separate):
    if phrase is None:
        raise Exception('Function is phrase but not given a phrase')
    result_dict[f'messages that contain {phrase}'] = []
    result_dict[f'% of messages that contain {phrase}'] = []
    df[f'includes {phrase}?'] = df['text'].apply(
        lambda msg: helpers.is_phrase_in(phrase, msg, case_sensitive, separate)
    )
    for member_name in chat_members:
        total_messages, non_reaction_messages = initialize_result_dict(member_name, df, result_dict)
        if total_messages > 0:
            word_messages = len(
                df[(df[f'includes {phrase}?']) & (df['sender'] == member_name)]
            )
            result_dict[f'messages that contain {phrase}'].append(word_messages)
            result_dict[f'% of messages that contain {phrase}'].append(
                round((word_messages / non_reaction_messages) * 100, 2)
            )
