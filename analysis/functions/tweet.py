from analysis.utils.initialize_result_dict import initialize_result_dict
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers


def main(result_dict, df, chat_members):
    result_dict['messages that are tweets'] = []
    result_dict['% of messages that are tweets'] = []
    df['is tweet?'] = df['text'].apply(helpers.is_tweet)
    for member_name in chat_members:
        _, non_reaction_messages = initialize_result_dict(member_name, df, result_dict)
        tweet_messages = len(
            df[(df['is tweet?']) & (df['sender'] == member_name)]
        )
        result_dict['messages that are tweets'].append(tweet_messages)
        result_dict['% of messages that are tweets'].append(
            round(helpers.safe_divide(tweet_messages, non_reaction_messages) * 100, 2)
        )
