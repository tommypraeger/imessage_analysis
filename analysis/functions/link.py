from analysis.utils.initialize_result_dict import initialize_result_dict
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers

def main(result_dict, df, chat_members):
    result_dict['messages that are links'] = []
    result_dict['% of messages that are links'] = []
    df['is link?'] = df['text'].apply(helpers.is_link)
    for member_name in chat_members:
        total_messages, non_reaction_messages = initialize_result_dict(member_name, df, result_dict)
        if total_messages > 0:
            link_messages = len(
                df[(df['is link?']) & (df['sender'] == member_name)]
            )
            result_dict['messages that are links'].append(link_messages)
            result_dict['% of messages that are links'].append(
                round((link_messages / non_reaction_messages) * 100, 2)
            )
