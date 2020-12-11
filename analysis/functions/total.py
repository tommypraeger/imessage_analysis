from analysis.utils.initialize_result_dict import initialize_result_dict
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers


def main(result_dict, df, chat_members):
    result_dict['total messages'] = []
    result_dict['% of all messages that are by this person'] = []
    for member_name in chat_members:
        total_messages, _ = initialize_result_dict(member_name, df, result_dict)
        result_dict['total messages'].append(total_messages)
    total_messages = sum(result_dict['total messages'])
    for i in range(len(result_dict['total messages'])):
        result_dict['% of all messages that are by this person'].append(
            round(helpers.safe_divide(result_dict['total messages'][i], total_messages) * 100, 2)
        )
