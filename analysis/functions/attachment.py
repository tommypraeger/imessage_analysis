from analysis.utils.initialize_result_dict import initialize_result_dict
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers


def main(result_dict, df, chat_members):
    result_dict['attachment messages'] = []
    result_dict['% of messages that are attachments'] = []
    df['is attachment?'] = df['type'].apply(helpers.is_attachment)
    for member_name in chat_members:
        _, non_reaction_messages = initialize_result_dict(member_name, df, result_dict)
        attachment_messages = len(
            df[(df['is attachment?']) & (df['sender'] == member_name)]
        )
        result_dict['attachment messages'].append(attachment_messages)
        result_dict['% of messages that are attachments'].append(
            round(helpers.safe_divide(attachment_messages, non_reaction_messages) * 100, 2)
        )
