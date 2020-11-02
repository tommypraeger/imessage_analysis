from analysis.utils.initialize_result_dict import initialize_result_dict
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers

def main(result_dict, df, chat_members):
    result_dict['total messages'] = []
    result_dict['non-reaction messages'] = []
    result_dict['% of all non-reaction messages that are by this person'] = []
    result_dict['reaction messages'] = []
    result_dict['% of all reaction messages that are by this person'] = []
    result_dict['% of messages that are reactions'] = []
    result_dict['reactions'] = []
    result_dict['like reacts'] = []
    result_dict['% of reactions that are like reacts'] = []
    result_dict['love reacts'] = []
    result_dict['% of reactions that are love reacts'] = []
    result_dict['dislike reacts'] = []
    result_dict['% of reactions that are dislike reacts'] = []
    result_dict['laugh reacts'] = []
    result_dict['% of reactions that are laugh reacts'] = []
    result_dict['emphasis reacts'] = []
    result_dict['% of reactions that are emphasis reacts'] = []
    result_dict['question reacts'] = []
    result_dict['% of reactions that are question reacts'] = []
    df['reaction action'] = df['text'].apply(helpers.reaction_action)
    df['like react action'] = df['text'].apply(helpers.like_react_action)
    df['love react action'] = df['text'].apply(helpers.love_react_action)
    df['dislike react action'] = df['text'].apply(helpers.dislike_react_action)
    df['laugh react action'] = df['text'].apply(helpers.laugh_react_action)
    df['emphasis react action'] = df['text'].apply(helpers.emphasis_react_action)
    df['question react action'] = df['text'].apply(helpers.question_react_action)
    for member_name in chat_members:
        total_messages, non_reaction_messages = initialize_result_dict(member_name, df, result_dict)
        if total_messages > 0:
            result_dict['total messages'].append(total_messages)
            result_dict['reaction messages'].append(total_messages - non_reaction_messages)
            result_dict['non-reaction messages'].append(non_reaction_messages)
            result_dict['% of messages that are reactions'].append(
                round((1 - (non_reaction_messages / total_messages)) * 100, 2)
            )
            reactions = df[df['sender'] == member_name]['reaction action'].sum()
            like_reacts = df[df['sender'] == member_name]['like react action'].sum()
            love_reacts = df[df['sender'] == member_name]['love react action'].sum()
            dislike_reacts = df[df['sender'] == member_name]['dislike react action'].sum()
            laugh_reacts = df[df['sender'] == member_name]['laugh react action'].sum()
            emphasis_reacts = df[df['sender'] == member_name]['emphasis react action'].sum()
            question_reacts = df[df['sender'] == member_name]['question react action'].sum()
            result_dict['reactions'].append(reactions)
            result_dict['like reacts'].append(like_reacts)
            result_dict['% of reactions that are like reacts'].append(
                round((like_reacts / reactions) * 100, 2)
            )
            result_dict['love reacts'].append(love_reacts)
            result_dict['% of reactions that are love reacts'].append(
                round((love_reacts / reactions) * 100, 2)
            )
            result_dict['dislike reacts'].append(dislike_reacts)
            result_dict['% of reactions that are dislike reacts'].append(
                round((dislike_reacts / reactions) * 100, 2)
            )
            result_dict['laugh reacts'].append(laugh_reacts)
            result_dict['% of reactions that are laugh reacts'].append(
                round((laugh_reacts / reactions) * 100, 2)
            )
            result_dict['emphasis reacts'].append(emphasis_reacts)
            result_dict['% of reactions that are emphasis reacts'].append(
                round((emphasis_reacts / reactions) * 100, 2)
            )
            result_dict['question reacts'].append(question_reacts)
            result_dict['% of reactions that are question reacts'].append(
                round((question_reacts / reactions) * 100, 2)
            )
    total_non_reaction_messages = sum(result_dict['non-reaction messages'])
    total_reaction_messages = sum(result_dict['reaction messages'])
    for i in range(len(result_dict['total messages'])):
        result_dict['% of all non-reaction messages that are by this person'].append(
            round((result_dict['non-reaction messages'][i] / total_non_reaction_messages) * 100, 2)
        )
        result_dict['% of all reaction messages that are by this person'].append(
            round((result_dict['reaction messages'][i] / total_reaction_messages) * 100, 2)
        )
