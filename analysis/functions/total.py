from analysis.utils.initialize_result_dict import initialize_result_dict
import analysis.utils.constants as constants

def main(result_dict, df):
    result_dict['total messages'] = []
    result_dict['% of all messages that are by this person'] = []
    for member_name in constants.CONTACT_IDS:
        total_messages, _ = initialize_result_dict(member_name, df, result_dict)
        if total_messages > 0:
            result_dict['total messages'].append(total_messages)
    total_messages = sum(result_dict['total messages'])
    for i in range(len(result_dict['total messages'])):
        result_dict['% of all messages that are by this person'].append(
            round((result_dict['total messages'][i] / total_messages) * 100, 2)
        )
