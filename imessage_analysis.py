import argparse
import sqlite3
import time

import numpy as np
import pandas as pd

from constants import *
from functions import *

start_time = time.time()

parser = argparse.ArgumentParser(description='run analysis on text messages')
parser.add_argument('name', type=str)
parser.add_argument('--csv', action='store_true', help='export data to csv')
parser.add_argument('--from-date', type=str, help='date to start from. format mmddyy')
parser.add_argument('--to-date', type=str, help='date to end at. format mmddyy')
parser.add_argument('--group', action='store_true', help='desired chat is a group chat')
parser.add_argument('--phrase', type=str, help='phrase to search for')
parser.add_argument('--separate', action='store_true', help='separate phrase into words')
parser.add_argument('--case-sensitive', action='store_true', help='make search case sensitive')
parser.add_argument('--type', type=str, help='MIME type of message to search for')
parser.add_argument('--print-messages', action='store_true', help='print found messages')
function_group = parser.add_mutually_exclusive_group()
function_group.add_argument('--function', type=str, help='name of function to call')
function_group.add_argument('--all-functions', action='store_true', help='call all functions')
args = parser.parse_args()

# Create SQL connection
conn = sqlite3.connect(f'/Users/{USERNAME}/Library/Messages/chat.db')
c = conn.cursor()

if args.group:
    CHAT_ID = CHAT_IDS[args.name]

    # Get chat history
    cmd1 = f'SELECT ROWID, text, handle_id, date \
                FROM message T1 \
                INNER JOIN chat_message_join T2 \
                    ON T2.chat_id={CHAT_ID} \
                    AND T1.ROWID=T2.message_id \
                ORDER BY T1.date'
    c.execute(cmd1)
    df_msg = pd.DataFrame(c.fetchall(), columns=['id', 'text', 'sender', 'time'])
    df_msg['sender'] = [
        CONTACT_ID_TO_NAME[sender] for sender in df_msg['sender']
    ]

    # Get attachment history
    cmd2 = f'SELECT T1.ROWID, T2.mime_type \
            FROM message T1 \
            INNER JOIN chat_message_join T3 \
                ON T1.ROWID=T3.message_id \
            INNER JOIN attachment T2 \
            INNER JOIN message_attachment_join T4 \
                ON T2.ROWID=T4.attachment_id \
                WHERE T4.message_id=T1.ROWID \
                AND (T3.chat_id={CHAT_ID})'
    c.execute(cmd2)
    df_att = pd.DataFrame(c.fetchall(), columns=['id', 'type'])
else:
    CHAT_ID = CHAT_IDS[args.name]
    CONTACT_ID = CONTACT_NAME_TO_ID[args.name]

    # Get chat history
    cmd1 = f'SELECT ROWID, text, is_from_me, date, is_read \
                FROM message T1 \
                INNER JOIN chat_message_join T2 \
                    ON T2.chat_id={CHAT_ID} \
                    AND T1.ROWID=T2.message_id \
                ORDER BY T1.date'
    c.execute(cmd1)
    df_msg = pd.DataFrame(c.fetchall(), columns=['id', 'text', 'sender', 'time', 'is_read'])
    df_msg['sender'] = [
        CONTACT_ID_TO_NAME[0] if sender == 1 else CONTACT_ID_TO_NAME[CONTACT_ID]
        for sender in df_msg['sender']
    ]

    # Get attachment history
    cmd2 = f'SELECT T1.ROWID, T2.mime_type \
            FROM message T1 \
            INNER JOIN chat_message_join T3 \
                ON T1.ROWID=T3.message_id \
            INNER JOIN attachment T2 \
            INNER JOIN message_attachment_join T4 \
                ON T2.ROWID=T4.attachment_id \
                WHERE T4.message_id=T1.ROWID \
                AND (T3.chat_id={CHAT_ID})'
    c.execute(cmd2)
    df_att = pd.DataFrame(c.fetchall(), columns=['id', 'type'])

# Create DataFrame
df = df_msg.set_index('id').join(df_att.set_index('id'))


if args.from_date:
    df = df[df['time'] >= date_to_time(args.from_date)]
if args.to_date:
    df = df[df['time'] <= date_to_time(args.to_date, end=True)]

# Set timezone and date format
df['time'] = [
    datetime.datetime.fromtimestamp((t + TIME_OFFSET) / 1e9)
    for t in df['time']
]

# Clean type column
df['type'] = [t if type(t) is str else 'text/plain' for t in df['type']]

result_dict = {
    'names': []
}

if args.function and args.function not in FUNCTIONS:
    raise Exception('Invalid function name')

if not args.function and not args.all_functions and not args.phrase and not args.type:
    args.function = 'total'

total_messages_dict = {}
non_reaction_messages_dict = {}
total_messages = 0
non_reaction_messages = 0

# Always add reaction column
df['is reaction?'] = df['text'].apply(is_reaction)


def initialize_result_dict(member_name):
    if len(df.loc[df['sender'] == member_name]) > 0:
        # Add names if not already there
        if member_name not in result_dict['names']:
            result_dict['names'].append(member_name)

        # Calculate total messages and non-reaction messages
        if member_name not in total_messages_dict.keys():
            total_messages_dict[member_name] = len(
                df[df['sender'] == member_name]
            )
            non_reaction_messages_dict[member_name] = len(
                df[(df['sender'] == member_name) & (~df['is reaction?'])]
            )
        global total_messages, non_reaction_messages
        total_messages = total_messages_dict[member_name]
        assert(total_messages > 0)
        non_reaction_messages = non_reaction_messages_dict[member_name]
        assert(non_reaction_messages > 0)

        return True
    return False


if args.function == 'total' or args.all_functions:
    result_dict['total messages'] = []
    result_dict['% of all messages that are by this person'] = []
    sort_key = 'total messages'
    for member_name in CONTACT_NAME_TO_ID.keys():
        if initialize_result_dict(member_name):
            result_dict['total messages'].append(total_messages)
    total_messages = sum(result_dict['total messages'])
    for i in range(len(result_dict['total messages'])):
        result_dict['% of all messages that are by this person'].append(
            round((result_dict['total messages'][i] / total_messages) * 100, 2)
        )

if args.function == 'reaction' or args.all_functions:
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
    df['reaction action'] = df['text'].apply(reaction_action)
    df['like react action'] = df['text'].apply(like_react_action)
    df['love react action'] = df['text'].apply(love_react_action)
    df['dislike react action'] = df['text'].apply(dislike_react_action)
    df['laugh react action'] = df['text'].apply(laugh_react_action)
    df['emphasis react action'] = df['text'].apply(emphasis_react_action)
    df['question react action'] = df['text'].apply(question_react_action)
    sort_key = 'reaction messages'
    for member_name in CONTACT_NAME_TO_ID.keys():
        if initialize_result_dict(member_name):
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

if args.function == 'attachment' or args.all_functions:
    result_dict['attachment messages'] = []
    result_dict['% of messages that are attachments'] = []
    sort_key = 'attachment messages'
    df['is attachment?'] = df['type'].apply(is_attachment)
    for member_name in CONTACT_NAME_TO_ID.keys():
        if initialize_result_dict(member_name):
            attachment_messages = len(
                df[(df['is attachment?']) & (df['sender'] == member_name)]
            )
            result_dict['attachment messages'].append(attachment_messages)
            result_dict['% of messages that are attachments'].append(
                round((attachment_messages / non_reaction_messages) * 100, 2)
            )

if args.function == 'emoji' or args.all_functions:
    result_dict['messages that contain emojis'] = []
    result_dict['% of messages that include emojis'] = []
    sort_key = 'messages that contain emojis'
    df['includes emoji?'] = df['text'].apply(includes_emoji)
    for member_name in CONTACT_NAME_TO_ID.keys():
        if initialize_result_dict(member_name):
            emoji_messages = len(
                df[(df['includes emoji?']) & (df['sender'] == member_name)]
            )
            result_dict['messages that contain emojis'].append(emoji_messages)
            result_dict['% of messages that include emojis'].append(
                round((emoji_messages / non_reaction_messages) * 100, 2)
            )

if args.function == 'all caps' or args.all_functions:
    result_dict['all caps messages'] = []
    result_dict['% of messages that are all caps'] = []
    sort_key = 'all caps messages'
    df['is all caps?'] = df['text'].apply(is_all_caps)
    for member_name in CONTACT_NAME_TO_ID.keys():
        if initialize_result_dict(member_name):
            all_caps_messages = len(
                df[(df['is all caps?']) & (df['sender'] == member_name)]
            )
            result_dict['all caps messages'].append(all_caps_messages)
            result_dict['% of messages that are all caps'].append(
                round((all_caps_messages / non_reaction_messages) * 100, 2)
            )

if args.function == 'convo starter' or args.all_functions:
    result_dict['convo starters'] = []
    result_dict['% of all convo starters that are by this person'] = []
    sort_key = 'convo starters'
    df['is convo starter?'] = df['time'].diff().apply(is_convo_starter)
    df.iloc[0, df.columns.get_loc('is convo starter?')] = True
    for member_name in CONTACT_NAME_TO_ID.keys():
        if initialize_result_dict(member_name):
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

if args.function == 'tweet' or args.all_functions:
    result_dict['messages that are tweets'] = []
    result_dict['% of messages that are tweets'] = []
    sort_key = 'messages that are tweets'
    df['is tweet?'] = df['text'].apply(is_tweet)
    for member_name in CONTACT_NAME_TO_ID.keys():
        if initialize_result_dict(member_name):
            tweet_messages = len(
                df[(df['is tweet?']) & (df['sender'] == member_name)]
            )
            result_dict['messages that are tweets'].append(tweet_messages)
            result_dict['% of messages that are tweets'].append(
                round((tweet_messages / non_reaction_messages) * 100, 2)
            )

if args.function == 'link' or args.all_functions:
    result_dict['messages that are links'] = []
    result_dict['% of messages that are links'] = []
    sort_key = 'messages that are links'
    df['is link?'] = df['text'].apply(is_link)
    for member_name in CONTACT_NAME_TO_ID.keys():
        if initialize_result_dict(member_name):
            link_messages = len(
                df[(df['is link?']) & (df['sender'] == member_name)]
            )
            result_dict['messages that are links'].append(link_messages)
            result_dict['% of messages that are links'].append(
                round((link_messages / non_reaction_messages) * 100, 2)
            )

if args.function == 'message word count' or args.all_functions:
    result_dict['average message word count'] = []
    sort_key = 'average message word count'
    if not args.all_functions:
        df['is attachment?'] = df['type'].apply(is_attachment)
        df['is link?'] = df['text'].apply(is_link)
    df['message word count'] = df['text'].apply(message_word_count)
    for member_name in CONTACT_NAME_TO_ID.keys():
        if initialize_result_dict(member_name):
            average_message_word_count = df[
                (df['sender'] == member_name)
                & (~df['is reaction?'])
                & (~df['is attachment?'])
                & (~df['is link?'])
            ]['message word count'].mean()
            result_dict['average message word count'].append(
                round(average_message_word_count, 1)
            )

if args.function == 'word length' or args.all_functions:
    result_dict['average word length'] = []
    sort_key = 'average word length'
    if not args.all_functions:
        df['is attachment?'] = df['type'].apply(is_attachment)
        df['is link?'] = df['text'].apply(is_link)
    df['word length'] = df['text'].apply(average_word_length)
    for member_name in CONTACT_NAME_TO_ID.keys():
        if initialize_result_dict(member_name):
            average_word_length = df[
                (df['sender'] == member_name)
                & (~df['is reaction?'])
                & (~df['is attachment?'])
                & (~df['is link?'])
            ]['word length'].mean()
            result_dict['average word length'].append(
                round(average_word_length, 1)
            )

if args.function == 'message series' or args.all_functions:
    result_dict['total # of message series'] = []
    result_dict['total messages'] = []
    result_dict['average messages per series'] = []
    sort_key = 'average messages per series'
    if not args.all_functions:
        df['is convo starter?'] = df['time'].diff().apply(is_convo_starter)
        df.iloc[0, df.columns.get_loc('is convo starter?')] = True
    df['is new message series?'] = df['sender'].apply(lambda x: True)
    df['is new message series?'] = df['is new message series?'].shift().where(
        df['sender'].shift() != df['sender'], False
    )
    df.iloc[0, df.columns.get_loc('is new message series?')] = True
    for member_name in CONTACT_NAME_TO_ID.keys():
        if initialize_result_dict(member_name):
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

if args.function == 'game' or args.all_functions:
    result_dict['messages that are games'] = []
    result_dict['% of messages that are games'] = []
    result_dict['messages that are game starts'] = []
    result_dict['% of messages that are game starts'] = []
    sort_key = 'messages that are games'
    df['is game message?'] = df.apply(lambda msg: is_game_message(msg.text, msg.type), axis=1)
    df['is game start?'] = df.apply(lambda msg: is_game_start(msg.text, msg.type), axis=1)
    for member_name in CONTACT_NAME_TO_ID.keys():
        if initialize_result_dict(member_name):
            game_messages = len(
                df[(df['is game message?']) & (df['sender'] == member_name)]
            )
            game_starts = len(
                df[(df['is game start?']) & (df['sender'] == member_name)]
            )
            result_dict['messages that are games'].append(game_messages)
            result_dict['% of messages that are games'].append(
                round((game_messages / non_reaction_messages) * 100, 2)
            )
            result_dict['messages that are game starts'].append(game_starts)
            result_dict['% of messages that are game starts'].append(
                round((game_starts / non_reaction_messages) * 100, 2)
            )

if args.phrase:
    PHRASE = args.phrase
    result_dict[f'messages that contain {PHRASE}'] = []
    result_dict[f'% of messages that contain {PHRASE}'] = []
    sort_key = f'messages that contain {PHRASE}'
    df[f'includes {PHRASE}?'] = df['text'].apply(
        lambda msg: is_phrase_in(PHRASE, msg, args.case_sensitive, args.separate)
    )
    for member_name in CONTACT_NAME_TO_ID.keys():
        if initialize_result_dict(member_name):
            word_messages = len(
                df[(df[f'includes {PHRASE}?']) & (df['sender'] == member_name)]
            )
            result_dict[f'messages that contain {PHRASE}'].append(word_messages)
            result_dict[f'% of messages that contain {PHRASE}'].append(
                round((word_messages / non_reaction_messages) * 100, 2)
            )

if args.type:
    TYPE = args.type
    result_dict[f'{TYPE} messages'] = []
    result_dict[f'% of messages that are type {TYPE}'] = []
    sort_key = f'{TYPE} messages'
    df[f'is type {TYPE}?'] = df['type'].apply(lambda typ: is_type(typ, TYPE))
    for member_name in CONTACT_NAME_TO_ID.keys():
        if initialize_result_dict(member_name):
            type_messages = len(
                df[(df[f'is type {TYPE}?']) & (df['sender'] == member_name)]
            )
            result_dict[f'{TYPE} messages'].append(type_messages)
            result_dict[f'% of messages that are type {TYPE}'].append(
                round((type_messages / non_reaction_messages) * 100, 2)
            )

if args.all_functions:
    sort_key = 'total messages'

result_df = pd.DataFrame(data=result_dict)
result_df.sort_values(by=[sort_key], inplace=True, ascending=False)
print(result_df.to_string(index=False))

# Export to CSV
if args.csv:
    df.to_csv('message_data.csv')
    result_df.to_csv('member_data.csv', index=False)
    result_df.corr(method='pearson').round(4).to_csv('correlation_matrix.csv')

print("--- %s seconds ---" % (time.time() - start_time))
