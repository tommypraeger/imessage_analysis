from analysis.utils.initialize_result_dict import initialize_result_dict
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers

def main(result_dict, df, mime_type):
    if mime_type is None:
        raise Exception('Function is type but not given a type')
    result_dict[f'{mime_type} messages'] = []
    result_dict[f'% of messages that are mime_type {mime_type}'] = []
    df[f'is mime_type {mime_type}?'] = df['type'].apply(lambda typ: helpers.is_type(typ, mime_type))
    for member_name in constants.CONTACT_NAME_TO_ID.keys():
        total_messages, non_reaction_messages = initialize_result_dict(member_name, df, result_dict)
        if total_messages > 0:
            mime_type_messages = len(
                df[(df[f'is mime_type {mime_type}?']) & (df['sender'] == member_name)]
            )
            result_dict[f'{mime_type} messages'].append(mime_type_messages)
            result_dict[f'% of messages that are mime_type {mime_type}'].append(
                round((mime_type_messages / non_reaction_messages) * 100, 2)
            )
