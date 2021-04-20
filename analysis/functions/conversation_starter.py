from analysis.utils.initialize_result_dict import initialize_result_dict
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers


def main(result_dict, df, chat_members, minutes_threshold):
    result_dict['conversation starters'] = []
    result_dict['% of all conversation starters that are by this person'] = []
    df['is conversation starter?'] = df['time'].diff().apply(
        lambda diff: helpers.is_conversation_starter(diff, minutes_threshold)
    )
    df.iloc[0, df.columns.get_loc('is conversation starter?')] = True
    for member_name in chat_members:
        initialize_result_dict(member_name, df, result_dict)
        conversation_starters = len(
            df[(df['is conversation starter?'])
               & (df['sender'] == member_name)
               & (~df['is reaction?'])]
        )
        result_dict['conversation starters'].append(conversation_starters)
    total_conversation_starters = sum(result_dict['conversation starters'])
    for i in range(len(result_dict['conversation starters'])):
        result_dict['% of all conversation starters that are by this person'].append(
            round(
                helpers.safe_divide(result_dict['conversation starters']
                                    [i], total_conversation_starters) * 100,
                2
            )
        )
