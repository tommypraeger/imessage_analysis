import math

from analysis.utils.initialize_result_dict import initialize_result_dict
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers


def main(result_dict, df, chat_members):
    result_dict['average word length'] = []
    df['is attachment?'] = df['type'].apply(helpers.is_attachment)
    df['is link?'] = df['text'].apply(helpers.is_link)
    df['word length'] = df['text'].apply(helpers.average_word_length)
    for member_name in chat_members:
        initialize_result_dict(member_name, df, result_dict)
        average_word_length = df[
            (df['sender'] == member_name)
            & (~df['is reaction?'])
            & (~df['is attachment?'])
            & (~df['is link?'])
        ]['word length'].mean()
        if math.isnan(average_word_length):
            average_word_length = 0
        result_dict['average word length'].append(
            round(average_word_length, 1)
        )
