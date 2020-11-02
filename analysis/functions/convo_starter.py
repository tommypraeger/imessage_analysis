from analysis.utils.initialize_result_dict import initialize_result_dict
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers

def main(result_dict, df, chat_members, minutes_threshold):
    result_dict['convo starters'] = []
    result_dict['% of all convo starters that are by this person'] = []
    df['is convo starter?'] = df['time'].diff().apply(
        lambda diff: helpers.is_convo_starter(diff, minutes_threshold)
    )
    df.iloc[0, df.columns.get_loc('is convo starter?')] = True
    for member_name in chat_members:
        total_messages, _ = initialize_result_dict(member_name, df, result_dict)
        if total_messages > 0:
            convo_starters = len(
                df[(df['is convo starter?'])
                & (df['sender'] == member_name)
                & (~df['is reaction?'])]
            )
            result_dict['convo starters'].append(convo_starters)
    total_convo_starters = sum(result_dict['convo starters'])
    for i in range(len(result_dict['convo starters'])):
        result_dict['% of all convo starters that are by this person'].append(
            round((result_dict['convo starters'][i] / total_convo_starters) * 100, 2)
        )
