from analysis.utils.constants import GRAPH_TOTAL_KEY
import analysis.utils.helpers as helpers

conversations_started_column = 'Conversations started'
percent_started_column = 'Percent of conversations started'


def get_columns():
    return [
        conversations_started_column,
        percent_started_column
    ]


def get_columns_allowing_graph_total():
    return [
        conversations_started_column
    ]


def main(result_dict, df, chat_members, args):
    result_dict[conversations_started_column] = []
    result_dict[percent_started_column] = []
    df['is conversation starter?'] = df['time'].diff().apply(
        lambda diff: helpers.is_conversation_starter(diff, args.minutes_threshold)
    )
    df.iloc[0, df.columns.get_loc('is conversation starter?')] = True
    for member_name in chat_members:
        helpers.initialize_member(member_name, result_dict)
        conversation_starters = len(
            df[(df['is conversation starter?'])
               & (df['sender'] == member_name)
               & (~df['is reaction?'])]
        )
        result_dict[conversations_started_column].append(conversation_starters)
    total_conversation_starters = sum(result_dict[conversations_started_column])
    for i in range(len(result_dict[conversations_started_column])):
        result_dict[percent_started_column].append(
            round(
                helpers.safe_divide(result_dict[conversations_started_column]
                                    [i], total_conversation_starters) * 100,
                2
            )
        )
