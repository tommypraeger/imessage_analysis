from analysis.utils.constants import GRAPH_TOTAL_KEY
import analysis.utils.helpers as helpers

total_messages_column = 'Total messages'
non_reaction_messages_column = 'Messages that are not reactions'
percent_all_non_reaction_column = 'Percent of all messages that are not reactions'
reactions_messages_column = 'Reaction messages (including removing reactions)'
percent_all_reactions_column = 'Percent of all reactions messages'
percent_reactions_column = 'Percent of messages that are reactions'
reactions_column = 'Reactions (not including removed reactions)'
likes_column = 'Like reacts'
percent_likes_column = 'Percent of reactions that are like reacts'
loves_column = 'Love reacts'
percent_loves_column = 'Percent of reactions that are love reacts'
dislikes_column = 'Dislike reacts'
percent_dislikes_column = 'Percent of reactions that are dislike reacts'
laughs_column = 'Laugh reacts'
percent_laugh_column = 'Percent of reactions that are laugh reacts'
emphasis_column = 'Emphasis reacts'
percent_emphasis_column = 'Percent of reactions that are emphasis reacts'
questions_column = 'Question reacts'
percent_questions_column = 'Percent of reactions that are question reacts'


def get_columns():
    return [
        total_messages_column,
        non_reaction_messages_column,
        percent_all_non_reaction_column,
        reactions_messages_column,
        percent_all_reactions_column,
        percent_reactions_column,
        reactions_column,
        likes_column,
        percent_likes_column,
        loves_column,
        percent_loves_column,
        dislikes_column,
        percent_dislikes_column,
        laughs_column,
        percent_laugh_column,
        emphasis_column,
        percent_emphasis_column,
        questions_column,
        percent_questions_column
    ]


def get_columns_allowing_graph_total():
    return [
        total_messages_column,
        non_reaction_messages_column,
        reactions_messages_column,
        percent_reactions_column,
        reactions_column,
        likes_column,
        percent_likes_column,
        loves_column,
        percent_loves_column,
        dislikes_column,
        percent_dislikes_column,
        laughs_column,
        percent_laugh_column,
        emphasis_column,
        percent_emphasis_column,
        questions_column,
        percent_questions_column
    ]


def process_df(df):
    df['reaction action'] = df['text'].apply(helpers.reaction_action)
    df['like react action'] = df['text'].apply(helpers.like_react_action)
    df['love react action'] = df['text'].apply(helpers.love_react_action)
    df['dislike react action'] = df['text'].apply(helpers.dislike_react_action)
    df['laugh react action'] = df['text'].apply(helpers.laugh_react_action)
    df['emphasis react action'] = df['text'].apply(helpers.emphasis_react_action)
    df['question react action'] = df['text'].apply(helpers.question_react_action)


def get_results(output_dict, df, member_name=None, time_period=None):
    total_messages = helpers.get_total_messages(df, member_name, time_period)
    nr_messages = helpers.get_total_non_reaction_messages(df, member_name, time_period)
    output_dict[total_messages_column].append(total_messages)
    reaction_messages = total_messages - nr_messages
    output_dict[reactions_messages_column].append(reaction_messages)
    output_dict[non_reaction_messages_column].append(nr_messages)
    output_dict[percent_reactions_column].append(
        round((1 - helpers.safe_divide(nr_messages, total_messages)) * 100, 2)
    )

    messages = helpers.get_messages(df, member_name, time_period)
    reactions = int(messages['reaction action'].sum())
    like_reacts = int(messages['like react action'].sum())
    love_reacts = int(messages['love react action'].sum())
    dislike_reacts = int(messages['dislike react action'].sum())
    laugh_reacts = int(messages['laugh react action'].sum())
    emphasis_reacts = int(messages['emphasis react action'].sum())
    question_reacts = int(messages['question react action'].sum())

    output_dict[reactions_column].append(reactions)

    output_dict[likes_column].append(like_reacts)
    output_dict[percent_likes_column].append(
        round(helpers.safe_divide(like_reacts, reactions) * 100, 2)
    )

    output_dict[loves_column].append(love_reacts)
    output_dict[percent_loves_column].append(
        round(helpers.safe_divide(love_reacts, reactions) * 100, 2)
    )

    output_dict[dislikes_column].append(dislike_reacts)
    output_dict[percent_dislikes_column].append(
        round(helpers.safe_divide(dislike_reacts, reactions) * 100, 2)
    )

    output_dict[laughs_column].append(laugh_reacts)
    output_dict[percent_laugh_column].append(
        round(helpers.safe_divide(laugh_reacts, reactions) * 100, 2)
    )

    output_dict[emphasis_column].append(emphasis_reacts)
    output_dict[percent_emphasis_column].append(
        round(helpers.safe_divide(emphasis_reacts, reactions) * 100, 2)
    )

    output_dict[questions_column].append(question_reacts)
    output_dict[percent_questions_column].append(
        round(helpers.safe_divide(question_reacts, reactions) * 100, 2)
    )

    return reaction_messages, nr_messages


def get_table_results(result_dict, df, chat_members, args):
    process_df(df)
    for member_name in chat_members:
        helpers.initialize_member(member_name, result_dict)
        get_results(result_dict, df, member_name)
    total_reaction_messages = sum(result_dict[reactions_messages_column])
    total_non_reaction_messages = sum(result_dict[non_reaction_messages_column])
    for i in range(len(result_dict[total_messages_column])):
        result_dict[percent_all_reactions_column].append(round(helpers.safe_divide(
            result_dict[reactions_messages_column][i],
            total_reaction_messages) * 100, 2))
        result_dict[percent_all_non_reaction_column].append(round(helpers.safe_divide(
            result_dict[non_reaction_messages_column][i],
            total_non_reaction_messages) * 100, 2))


def get_graph_results(graph_data, df, chat_members, time_periods, args):
    process_df(df)
    if args.graph_individual:
        get_individual_graph_results(graph_data, df, chat_members, time_periods)
    else:
        get_total_graph_results(graph_data, df, time_periods)


def get_individual_graph_results(graph_data, df, chat_members, time_periods):
    for time_period in time_periods:
        total_reaction_messages_in_period = 0
        total_non_reaction_messages_in_period = 0
        for member_name in chat_members:
            member_reaction_messages_in_period, member_nr_messages_in_period = get_results(
                graph_data[member_name], df, member_name, time_period)
            total_reaction_messages_in_period += member_reaction_messages_in_period
            total_non_reaction_messages_in_period += member_nr_messages_in_period
        for member_name in chat_members:
            graph_data[member_name][percent_all_reactions_column].append(
                round(helpers.safe_divide(
                    graph_data[member_name][reactions_messages_column][-1],
                    total_reaction_messages_in_period) * 100, 2))
            graph_data[member_name][percent_all_non_reaction_column].append(
                round(helpers.safe_divide(
                    graph_data[member_name][non_reaction_messages_column][-1],
                    total_non_reaction_messages_in_period) * 100, 2))


def get_total_graph_results(graph_data, df, time_periods):
    for time_period in time_periods:
        get_results(graph_data[GRAPH_TOTAL_KEY], df, None, time_period)
