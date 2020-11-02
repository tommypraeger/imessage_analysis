from analysis.utils.initialize_result_dict import initialize_result_dict
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers

def main(result_dict, df, chat_members, running_all_functions, minutes_threshold):
    result_dict['total # of message series'] = []
    result_dict['total messages'] = []
    result_dict['average messages per series'] = []
    if not running_all_functions:
        df['is convo starter?'] = df['time'].diff().apply(
            lambda diff: helpers.is_convo_starter(diff, minutes_threshold)
        )
        df.iloc[0, df.columns.get_loc('is convo starter?')] = True
    df['is new message series?'] = df['sender'].apply(lambda x: True)
    df['is new message series?'] = df['is new message series?'].shift().where(
        df['sender'].shift() != df['sender'], False
    )
    df.iloc[0, df.columns.get_loc('is new message series?')] = True
    for member_name in chat_members:
        total_messages, _ = initialize_result_dict(member_name, df, result_dict)
        if total_messages > 0:
            message_series = len(
                df[((df['is new message series?'])
                | (df['is convo starter?']))
                & (df['sender'] == member_name)]
            )
            result_dict['total # of message series'].append(message_series)
            result_dict['total messages'].append(total_messages)
            result_dict['average messages per series'].append(
                round((total_messages / message_series), 2)
            )
