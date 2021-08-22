from analysis.utils.initialize_result_dict import initialize_result_dict
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers


def main(result_dict, df, chat_members, args):
    mime_type = args.mime_type
    if mime_type is None:
        raise Exception('Function is type but not given a type')
    result_dict[f'{mime_type} messages'] = []
    result_dict[f'% of messages that are file type {mime_type}'] = []
    df[f'is file type {mime_type}?'] = df['type'].apply(lambda typ: helpers.is_type(typ, mime_type))
    for member_name in chat_members:
        _, non_reaction_messages = initialize_result_dict(member_name, df, result_dict)
        mime_type_messages = len(
            df[(df[f'is file type {mime_type}?']) & (df['sender'] == member_name)]
        )
        result_dict[f'{mime_type} messages'].append(mime_type_messages)
        result_dict[f'% of messages that are file type {mime_type}'].append(
            round(helpers.safe_divide(mime_type_messages, non_reaction_messages) * 100, 2)
        )
