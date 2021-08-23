import math

from analysis.utils.initialize_result_dict import initialize_result_dict
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers


def main(result_dict, df, chat_members):
    result_dict['average word count'] = []
    df['is attachment?'] = df['type'].apply(helpers.is_attachment)
    df['is link?'] = df['text'].apply(helpers.is_link)
    df['word count'] = df['text'].apply(helpers.message_word_count)
    for member_name in chat_members:
        initialize_result_dict(member_name, df, result_dict)
        average_message_word_count = df[
            (df['sender'] == member_name)
            & (~df['is reaction?'])
            & (~df['is attachment?'])
            & (~df['is link?'])
        ]['word count'].mean()
        if math.isnan(average_message_word_count):
            average_message_word_count = 0
        result_dict['average word count'].append(
            round(average_message_word_count, 1)
        )
