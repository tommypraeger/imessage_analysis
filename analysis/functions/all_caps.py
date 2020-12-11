from analysis.utils.initialize_result_dict import initialize_result_dict
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers


def main(result_dict, df, chat_members):
    result_dict['all caps messages'] = []
    result_dict['% of messages that are all caps'] = []
    df['is all caps?'] = df['text'].apply(helpers.is_all_caps)
    for member_name in chat_members:
        _, non_reaction_messages = initialize_result_dict(member_name, df, result_dict)
        all_caps_messages = len(
            df[(df['is all caps?']) & (df['sender'] == member_name)]
        )
        result_dict['all caps messages'].append(all_caps_messages)
        result_dict['% of messages that are all caps'].append(
            round(helpers.safe_divide(all_caps_messages, non_reaction_messages) * 100, 2)
        )
