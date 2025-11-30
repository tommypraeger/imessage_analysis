import sqlite3
from functools import wraps
import pandas as pd

from src.utils import helpers


def _db_uri_readonly() -> str:
    path = f"/Users/{helpers.get_username()}/Library/Messages/chat.db"
    return f"file:{path}?mode=ro"


def _connect():
    """Returns a read-only sqlite3 connection for pandas/SQL reads."""
    return sqlite3.connect(_db_uri_readonly(), uri=True)


def with_ro_conn(fn):
    """Decorator that injects a read-only sqlite3 connection.

    - If a `conn` kwarg is provided, it's reused and not closed here.
    - Otherwise a new read-only connection is opened and closed around the call.
    """

    @wraps(fn)
    def wrapper(*args, conn=None, **kwargs):
        if conn is not None:
            return fn(*args, conn=conn, **kwargs)
        with _connect() as ro_conn:
            return fn(*args, conn=ro_conn, **kwargs)

    return wrapper


def test_db():
    """Attempt to open the Messages DB read-only and run a trivial query.

    Returns a tuple (code, message) where code=0 indicates success.
    """
    try:
        with _connect() as conn:
            # Probe a known table to confirm schema access; LIMIT keeps it cheap.
            conn.execute("SELECT ROWID FROM handle LIMIT 1")
        return 0, "Database has sufficient permissions."
    except sqlite3.OperationalError:
        ret = "\n===================================\n\n"
        ret += "There was an error accessing the Messages database in read-only mode.\n"

        ret += "\nIf you do not want to access the messages database, "
        ret += "you can pass --skip-mac-setup to the install.py script. "
        ret += "You would then only be able to use this program by providing a CSV of messages. "
        ret += "See the README for more details.\n"

        ret += "\nIf you are using a Mac and do want to access the Messages database, do the following:\n"
        ret += "1. Open System Settings\n"
        ret += "2. Go to Privacy & Security\n"
        ret += "3. Go to Full Disk Access\n"
        ret += (
            "4. Give Terminal (or whatever application you're running this from) Full Disk Access, ",
        )
        ret += "and then run the install.py script again.\n"
        ret += "\nNote: The app connects to the Messages database using read-only permissions.\n"
        ret += "\n===================================\n"
        return 1, ret


# Create DataFrame
@with_ro_conn
def get_df(name, group, *, conn):
    """Read messages and attachments in one pass via SQL and map sender names vectorized.

    - Uses parameterized IN for chat ids
    - LEFT JOIN attachments to avoid a second query
    - Maps sender using `is_from_me` + `handle_id` → contact name via a prebuilt dict
    """
    chat_ids = helpers.get_chat_ids()[name]
    placeholders = ",".join(["?"] * len(chat_ids))
    query = f"""
        SELECT m.ROWID AS id,
               m.text,
               m.is_from_me,
               m.handle_id,
               m.date AS time,
               m.guid,
               m.associated_message_guid AS reaction_to,
               m.associated_message_type AS message_type,
               m.attributedBody AS attributed_body,
               att.mime_type AS type
        FROM message m
        INNER JOIN chat_message_join cmj
            ON cmj.message_id = m.ROWID AND cmj.chat_id IN ({placeholders})
        LEFT JOIN message_attachment_join maj ON maj.message_id = m.ROWID
        LEFT JOIN attachment att ON att.ROWID = maj.attachment_id
        ORDER BY m.date
    """
    df = pd.read_sql_query(query, conn, params=chat_ids)

    # Maps contact IDs to names
    id_to_name = {
        contact_id: name
        for name, contact_ids in helpers.get_contact_ids().items()
        for contact_id in contact_ids
    }
    # Use handle_id unless is_from_me == 1, in which case 0
    # Ensure integer dtype compatibility
    sender_id = df["handle_id"].astype("Int64")
    sender_id = sender_id.mask(df["is_from_me"] == 1, 0)
    df["sender"] = sender_id.map(id_to_name)

    # Final column order roughly matching previous shape
    # Keep columns needed downstream
    cols = [
        "id",
        "text",
        "sender",
        "time",
        "guid",
        "reaction_to",
        "message_type",
        "attributed_body",
        "type",
    ]
    df = df[cols]
    return df


@with_ro_conn
def get_chat_members(chat_ids, *, conn):
    placeholders = ",".join(["?"] * len(chat_ids))
    cmd = f"SELECT handle_id FROM chat_handle_join WHERE chat_id IN ({placeholders})"
    cur = conn.execute(cmd, chat_ids)
    member_ids = cur.fetchall()
    member_ids = [int(member_id[0]) for member_id in member_ids]
    member_ids.append(0)
    member_names = [helpers.contact_name_from_id(member_id) for member_id in member_ids]
    return member_names


@with_ro_conn
def get_contact_ids_from_phone_number(phone_number, *, conn):
    cmd = "SELECT ROWID FROM handle WHERE id LIKE ?"
    cur = conn.execute(cmd, (f"%{phone_number}%",))
    contact_ids = cur.fetchall()
    return [int(contact_id[0]) for contact_id in contact_ids]


@with_ro_conn
def get_chat_ids_from_phone_number(phone_number, *, conn):
    cmd = "SELECT ROWID FROM chat WHERE chat_identifier LIKE ?"
    cur = conn.execute(cmd, (f"%{phone_number}%",))
    chat_ids = cur.fetchall()
    return [int(chat_id[0]) for chat_id in chat_ids]


@with_ro_conn
def get_chat_ids_from_chat_name(chat_name, *, conn):
    cmd = "SELECT ROWID FROM chat WHERE display_name = ?"
    cur = conn.execute(cmd, (chat_name,))
    chat_ids = cur.fetchall()
    return [int(chat_id[0]) for chat_id in chat_ids]


@with_ro_conn
def get_phone_number_from_contact_id(contact_id, *, conn):
    cmd = "SELECT id FROM handle WHERE ROWID = ?"
    cur = conn.execute(cmd, (contact_id,))
    return str(cur.fetchone())


@with_ro_conn
def get_all_phone_numbers(*, conn):
    cmd = "SELECT DISTINCT id FROM handle"
    cur = conn.execute(cmd)
    phone_numbers = cur.fetchall()
    return [str(phone_number[0]) for phone_number in phone_numbers]


@with_ro_conn
def get_all_chat_names(*, conn):
    cmd = 'SELECT DISTINCT display_name FROM chat WHERE display_name LIKE "_%";'
    cur = conn.execute(cmd)
    chat_names = cur.fetchall()
    return [str(chat_name[0]) for chat_name in chat_names]
