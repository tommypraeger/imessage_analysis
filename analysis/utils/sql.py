import sqlite3
import pandas as pd

import analysis.utils.constants as constants
import analysis.utils.helpers as helpers


# Create SQL connection
def connect_to_db():
    conn = sqlite3.connect(f"/Users/{constants.USERNAME}/Library/Messages/chat.db")
    return conn.cursor()


# Test DB
def test_db():
    c = connect_to_db()
    cmd = "SELECT * FROM handle"
    c.execute(cmd)


# Create DataFrame
def get_df(name, group):
    if group:
        df_msg, df_att = get_group_df(name)
    else:
        df_msg, df_att = get_individual_df(name)

    return df_msg.set_index("id").join(df_att.set_index("id"))


def get_group_df(name):
    c = connect_to_db()
    chat_ids = constants.CHAT_IDS[name]

    # Get chat history
    cmd1 = f'SELECT ROWID, text, handle_id, date \
                FROM message T1 \
                INNER JOIN chat_message_join T2 \
                    ON T2.chat_id IN ({",".join([str(chat_id) for chat_id in chat_ids])}) \
                    AND T1.ROWID=T2.message_id \
                ORDER BY T1.date'
    c.execute(cmd1)
    df_msg = pd.DataFrame(c.fetchall(), columns=["id", "text", "sender", "time"])
    df_msg["sender"] = [
        helpers.contact_name_from_id(sender) for sender in df_msg["sender"]
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
                AND (T3.chat_id IN ({",".join([str(chat_id) for chat_id in chat_ids])}))'
    c.execute(cmd2)
    df_att = pd.DataFrame(c.fetchall(), columns=["id", "type"])

    return df_msg, df_att


def get_individual_df(name):
    c = connect_to_db()
    chat_ids = constants.CHAT_IDS[name]
    # Doesn't matter which contact ID we use, all will map to same name
    contact_id = constants.CONTACT_IDS[name][0]

    # Get chat history
    cmd1 = f'SELECT ROWID, text, is_from_me, date \
                FROM message T1 \
                INNER JOIN chat_message_join T2 \
                    ON T2.chat_id IN ({",".join([str(chat_id) for chat_id in chat_ids])}) \
                    AND T1.ROWID=T2.message_id \
                ORDER BY T1.date'
    c.execute(cmd1)
    df_msg = pd.DataFrame(c.fetchall(), columns=["id", "text", "sender", "time"])
    df_msg["sender"] = [
        helpers.contact_name_from_id(0)
        if sender == 1
        else helpers.contact_name_from_id(contact_id)
        for sender in df_msg["sender"]
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
                AND (T3.chat_id IN ({",".join([str(chat_id) for chat_id in chat_ids])}))'
    c.execute(cmd2)
    df_att = pd.DataFrame(c.fetchall(), columns=["id", "type"])

    return df_msg, df_att


def get_chat_members(chat_ids):
    c = connect_to_db()
    cmd = f'SELECT handle_id \
            FROM chat_handle_join \
            WHERE chat_id IN ({",".join([str(chat_id) for chat_id in chat_ids])})'
    c.execute(cmd)
    member_ids = c.fetchall()
    member_ids = [int(member_id[0]) for member_id in member_ids]
    member_ids.append(0)
    member_names = [helpers.contact_name_from_id(member_id) for member_id in member_ids]
    return member_names


def get_contact_ids_from_phone_number(phone_number):
    c = connect_to_db()
    cmd = f'SELECT ROWID \
            FROM handle \
            WHERE id like "%{phone_number}%"'
    c.execute(cmd)
    contact_ids = c.fetchall()
    return [int(contact_id[0]) for contact_id in contact_ids]


def get_chat_ids_from_phone_number(phone_number):
    c = connect_to_db()
    cmd = f'SELECT ROWID \
            FROM chat \
            WHERE chat_identifier like "%{phone_number}%"'
    c.execute(cmd)
    chat_ids = c.fetchall()
    return [int(chat_id[0]) for chat_id in chat_ids]


def get_chat_ids_from_chat_name(chat_name):
    c = connect_to_db()
    cmd = f'SELECT ROWID \
            FROM chat \
            WHERE display_name="{chat_name}"'
    c.execute(cmd)
    chat_ids = c.fetchall()
    return [int(chat_id[0]) for chat_id in chat_ids]


def get_phone_number_from_contact_id(contact_id):
    c = connect_to_db()
    cmd = f"SELECT id \
            FROM handle \
            WHERE ROWID={contact_id}"
    c.execute(cmd)
    return str(c.fetchone())


def get_all_phone_numbers():
    c = connect_to_db()
    cmd = 'SELECT DISTINCT chat_identifier \
           FROM chat \
           WHERE chat_identifier NOT LIKE "chat%"'
    c.execute(cmd)
    phone_numbers = c.fetchall()
    return [str(phone_number[0]) for phone_number in phone_numbers]


def get_all_chat_names():
    c = connect_to_db()
    cmd = 'SELECT DISTINCT display_name \
           FROM chat \
           WHERE display_name LIKE "_%";'
    c.execute(cmd)
    chat_names = c.fetchall()
    return [str(chat_name[0]) for chat_name in chat_names]
