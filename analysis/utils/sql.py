import sqlite3
import pandas as pd

import analysis.utils.constants as constants
import analysis.utils.helpers as helpers


# Create SQL connection
conn = sqlite3.connect(f'/Users/{constants.USERNAME}/Library/Messages/chat.db')
c = conn.cursor()


# Test DB
def test_db():
    cmd = 'SELECt * from handle'
    c.execute(cmd)
    conn.close()


# Create DataFrame
def get_df(name, group):
    if group:
        df_msg, df_att = get_group_df(name)
    else:
        df_msg, df_att = get_individual_df(name)

    conn.close()
    return df_msg.set_index('id').join(df_att.set_index('id'))


def get_group_df(name):
    chat_ids = constants.CHAT_IDS[name]

    # Get chat history
    cmd1 = f'SELECT ROWID, text, handle_id, date \
                FROM message T1 \
                INNER JOIN chat_message_join T2 \
                    ON T2.chat_id IN ({",".join(chat_ids)}) \
                    AND T1.ROWID=T2.message_id \
                ORDER BY T1.date'
    c.execute(cmd1)
    df_msg = pd.DataFrame(c.fetchall(), columns=['id', 'text', 'sender', 'time'])
    df_msg['sender'] = [
        helpers.contact_name_from_id(sender) for sender in df_msg['sender']
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
                AND (T3.chat_id IN ({",".join(chat_ids)}))'
    c.execute(cmd2)
    df_att = pd.DataFrame(c.fetchall(), columns=['id', 'type'])

    return df_msg, df_att


def get_individual_df(name):
    chat_ids = constants.CHAT_IDS[name]
    # Doesn't matter which contact ID we use, all will map to same name
    contact_id = constants.CONTACT_IDS[name][0]

    # Get chat history
    cmd1 = f'SELECT ROWID, text, is_from_me, date, is_read \
                FROM message T1 \
                INNER JOIN chat_message_join T2 \
                    ON T2.chat_id IN ({",".join(chat_ids)}) \
                    AND T1.ROWID=T2.message_id \
                ORDER BY T1.date'
    c.execute(cmd1)
    df_msg = pd.DataFrame(c.fetchall(), columns=['id', 'text', 'sender', 'time', 'is_read'])
    df_msg['sender'] = [
        helpers.contact_name_from_id(0) if sender == 1 else helpers.contact_name_from_id(contact_id)
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
                AND (T3.chat_id IN ({",".join(chat_ids)}))'
    c.execute(cmd2)
    df_att = pd.DataFrame(c.fetchall(), columns=['id', 'type'])

    return df_msg, df_att
