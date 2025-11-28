import datetime
import json
import re
import string
import traceback

import pandas as pd

from typedstream.stream import TypedStreamReader

from src.utils import constants, sql

USERNAME = ""
CONTACT_IDS = ""
CHAT_IDS = ""


def initialize_member(member_name, result_dict):
    if member_name not in result_dict["Names"]:
        result_dict["Names"].append(member_name)


def get_messages(df, member_name=None, time_period=None):
    # Vectorized filter: exclude edits (messages starting with "Edited to")
    # TODO: find way to link edits to the original message
    # TODO: find better way to identify edits
    text_series = df["text"].astype("string")
    condition = ~text_series.str.startswith("Edited to", na=False)
    if time_period is not None:
        condition &= (df["time_period"] == time_period)
    if member_name is not None:
        condition &= (df["sender"] == member_name)
    return df[condition]


def get_non_reaction_messages(df, member_name=None, time_period=None):
    msgs = get_messages(df, member_name, time_period)
    mt = msgs["message_type"].astype("string")
    non_removed = ~mt.str.startswith("removed", na=False)
    non_reaction = ~mt.isin(constants.REACTION_TYPES)
    return msgs[non_removed & non_reaction]


def get_total_messages(df, member_name=None, time_period=None):
    return len(get_messages(df, member_name, time_period))


def get_total_non_reaction_messages(df, member_name=None, time_period=None):
    return len(get_non_reaction_messages(df, member_name, time_period))


def contact_name_from_id(contact_id):
    contact_ids = get_contact_ids()
    for name in contact_ids:
        if contact_id in contact_ids[name]:
            return name
    return sql.get_phone_number_from_contact_id(contact_id)


def load_user_data():
    with open(constants.USER_DATA_FILE_NAME, "r") as user_data_file:
        user_data = json.load(user_data_file)
    return user_data


def get_username():
    global USERNAME
    if USERNAME == "":
        user_data = load_user_data()
        USERNAME = user_data["username"]
    return USERNAME


def get_contact_ids():
    global CONTACT_IDS
    if CONTACT_IDS == "":
        user_data = load_user_data()
        CONTACT_IDS = user_data["contact_ids"]
    return CONTACT_IDS


def get_chat_ids():
    global CHAT_IDS
    if CHAT_IDS == "":
        user_data = load_user_data()
        CHAT_IDS = user_data["chat_ids"]
    return CHAT_IDS


def save_user_data(user_data):
    with open(constants.USER_DATA_FILE_NAME, "w") as user_data_file:
        json.dump(user_data, user_data_file, indent=4)


def clean_phone_number(phone_number):
    if "@" in phone_number:
        # actually an email
        return phone_number
    digits = [i for i in phone_number if i.isdigit()]
    return "".join(digits)[-10:]


def make_error_message(msg):
    if isinstance(msg, Exception):
        return {"errorMessage": f"{str(msg)}\n{traceback.format_exc()}"}
    return {"errorMessage": str(msg)}


def make_success_message(msg):
    return {"successMessage": str(msg)}


def safe_divide(numerator, denominator):
    """
    Does division but returns 0 if denominator is 0
    """
    if denominator == 0:
        return 0

    return numerator / denominator


def safe_divide_as_pct(numerator, denominator):
    return round(
        safe_divide(numerator, denominator) * 100,
        2,
    )


def parse_date(date_str):
    # remove fractions of second
    # assuming dates are not using dots
    date_str = date_str.split(".")[0]
    for fmt in constants.DATE_FORMATS:
        try:
            return datetime.datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError("invalid date format")


def date_to_time(date, end_of_day=None):
    date = parse_date(date)
    if end_of_day is None:
        timestamp = date.timestamp()
    if end_of_day:
        timestamp = datetime.datetime(
            date.year, date.month, date.day, 23, 59, 59
        ).timestamp()
    else:
        timestamp = datetime.datetime(date.year, date.month, date.day).timestamp()

    return timestamp * 1e9




def is_reaction(message_type):
    message_type = str(message_type)
    return message_type in constants.REACTION_TYPES


def is_removed_reaction(message_type):
    message_type = str(message_type)
    return message_type.startswith("removed")




def is_phrase_in(phrase, msg, message_type, case_sensitive, separate, regex):
    if is_reaction(message_type):
        return False
    msg = str(msg)
    if regex:
        if re.search(phrase, msg):
            return True
        else:
            return False

    if not any(char in string.punctuation for char in phrase):
        msg = msg.translate(str.maketrans("", "", string.punctuation))

    if not case_sensitive:
        msg = msg.lower()
        phrase = phrase.lower()

    if separate:
        msg = msg.split()
        phrase = phrase.split()
        return is_sub_list(phrase, msg)
    else:
        return phrase in msg


def is_sub_list(small, big):
    if len(small) > len(big):
        return False
    small_length = len(small)
    for i in range(len(big) - small_length + 1):
        if big[i : i + small_length] == small:
            return True
    return False






# huge thank you to this reddit comment and the post as a whole
# https://www.reddit.com/r/osx/comments/uevy32/comment/kie8ccz
def decode_message_attributedbody(data):
    if not data:
        return None
    for event in TypedStreamReader.from_data(data):
        # The first bytes object is the one we want
        if type(event) is bytes:
            return event.decode("utf-8")


def add_reactions_for_each_message(df):
    """
    Given a DataFrame of messages + reactions, return only the original (non-reaction)
    messages enriched with two columns:

    - "reaction_count": total number of reactions that message received
    - "reactions_per_user": list of (reactor_name, reaction_type) tuples for that message

    Notes
    - Reaction rows are identified by message_type ∈ constants.REACTION_TYPES and are
      matched back to the original message via the "reaction_to" column.
    - Some databases prefix reaction_to with "p:0/"; we normalize by stripping that
      prefix so it matches the original message "guid" column.
    - Removed reactions (message_type starting with "removed …") are not counted here;
      only actual reaction rows in REACTION_TYPES are considered.

    Example (schematic)
    - Originals:  g1 (Alice), g2 (Bob)
    - Reactions:  like(Bob → g1), like(Carol → g1), laugh(Alice → g2)
    Output rows for g1 and g2 include reaction_count and reactions_per_user
    such as:
      g1: reaction_count=2, reactions_per_user=[("Bob", "like"), ("Carol", "like")]
      g2: reaction_count=1, reactions_per_user=[("Alice", "laugh")]
    """

    # Select only reaction rows and normalize their reaction_to GUIDs
    message_type_series = df["message_type"].astype("string")
    reactions_df = df[message_type_series.isin(constants.REACTION_TYPES)].copy()
    reactions_df["reaction_to"] = (
        reactions_df["reaction_to"].astype("string").str.replace(r"^p:0/", "", regex=True)
    )

    # Build aggregations keyed by the original message guid that was reacted to
    # 1) reaction_counts_by_guid: guid -> number of reactions
    # 2) reactions_by_guid: guid -> list[(reactor_name, reaction_type)]
    reaction_counts_by_guid = reactions_df.groupby("reaction_to").size()
    reactions_by_guid = reactions_df.groupby("reaction_to").apply(
        lambda g: list(zip(g["sender"].tolist(), g["message_type"].tolist()))
    )

    # Keep only original messages (not reactions) and enrich them with the aggregations
    originals_df = df[df["reaction_to"].isna()].copy()
    originals_df["reaction_count"] = (
        originals_df["guid"].map(reaction_counts_by_guid).fillna(0).astype("int64")
    )
    mapped_reactions_list = originals_df["guid"].map(reactions_by_guid)
    originals_df["reactions_per_user"] = mapped_reactions_list.apply(
        lambda x: x if isinstance(x, list) else []
    )
    return originals_df


def compute_conversation_columns(df, minutes_threshold=None):
    """
    Mutates and returns df with two columns:
      - "is conversation starter?": True only for non-reaction rows that start a conversation
      - "conversation number": 1-based consecutive conversation id across all rows

    Rules:
      - Only non-reaction messages can start conversations (gap > threshold or first non-reaction)
      - Reactions are assigned to the same conversation as their parent message (via reaction_to)
    """

    if minutes_threshold is None:
        minutes_threshold = constants.DEFAULT_CONVERSATION_STARTER_THRESHOLD_MINUTES

    # Determine reaction flags (including removed reactions)
    mt = df.get("message_type")
    mt = mt.astype("string") if mt is not None else pd.Series([""] * len(df), index=df.index, dtype="string")
    is_removed = mt.str.startswith("removed", na=False)
    is_reaction_type = mt.isin(constants.REACTION_TYPES)
    is_reaction_row = (is_removed | is_reaction_type)

    # Compute starters among non-reaction rows only
    non_reaction_idx = df.index[~is_reaction_row]
    starters = pd.Series(False, index=df.index)
    if len(non_reaction_idx) > 0:
        times = df.loc[non_reaction_idx, "time"]
        # Vectorized diff in seconds among non-reactions
        seconds = times.diff().dt.total_seconds()
        starters_nr = seconds.gt(minutes_threshold * 60)
        starters_nr.loc[seconds.isna()] = True
        starters.loc[non_reaction_idx] = starters_nr
    # Reactions never start conversations
    starters.loc[is_reaction_row] = False
    df["is conversation starter?"] = starters

    # Conversation number: cumsum of starters on non-reactions, propagate to all rows
    conv = pd.Series(pd.NA, index=df.index, dtype="Int64")
    if len(non_reaction_idx) > 0:
        conv_nr = starters.loc[non_reaction_idx].astype("int64").cumsum()
        # Start from 1 (first non-reaction should be True -> 1). In case it isn't, coerce min to 1.
        if len(conv_nr) > 0 and conv_nr.iloc[0] == 0:
            conv_nr = conv_nr + 1
        conv.loc[non_reaction_idx] = conv_nr.astype("Int64")

    # Attempt to map reactions to their parent conversation via reaction_to
    # Normalize GUIDs similarly to add_reactions_for_each_message
    guid_norm = df.get("guid").astype("string").str.replace(r"^p:0/", "", regex=True) if "guid" in df.columns else None
    reaction_to = df.get("reaction_to")
    reaction_to_norm = (
        reaction_to.astype("string").str.replace(r"^p:0/", "", regex=True)
        if reaction_to is not None
        else None
    )
    if guid_norm is not None and reaction_to_norm is not None:
        # Build map from base message guid -> conversation number (non-reactions only)
        base_guid_to_conv = {}
        for g, c in zip(guid_norm.loc[non_reaction_idx], conv.loc[non_reaction_idx]):
            if pd.notna(c):
                base_guid_to_conv[str(g)] = int(c)
        # Assign mapped conversation numbers to reactions where possible
        reaction_idx = df.index[is_reaction_row]
        if len(reaction_idx) > 0:
            mapped = reaction_to_norm.loc[reaction_idx].map(base_guid_to_conv)
            # Prefer explicit parent mapping; otherwise leave as NA to be filled below
            for i, val in mapped.items():
                if pd.notna(val):
                    conv.loc[i] = int(val)

    # Fallback: forward-fill conversation numbers by time so reactions inherit nearest prior conversation
    # This also covers reactions with missing/invalid parent mappings (e.g., CSV inputs without reaction_to)
    conv = conv.ffill()
    # If still NA at beginning, back-fill
    conv = conv.bfill()
    # Final safety: set any remaining NA to 1
    conv = conv.fillna(1)
    df["conversation number"] = conv.astype("int64")

    return df


def summarize_conversations(df, time_period=None):
    """
    Return (participants_by_conversation, starter_by_conversation, member_conversations)
    using the conversation columns populated by compute_conversation_columns.
    """
    msgs = get_messages(df, time_period=time_period)
    msgs = msgs[msgs["sender"].notna()].copy()
    if "conversation number" not in msgs.columns:
        return {}, {}, {}
    participants_by_conv = {}
    starter_by_conv = {}
    grouped = msgs.groupby("conversation number", dropna=True)
    for conv_id, group in grouped:
        if pd.isna(conv_id):
            continue
        conv_int = int(conv_id)
        senders = group["sender"].dropna().astype("string")
        if len(senders) == 0:
            continue
        participants = set(str(s) for s in senders)
        participants_by_conv[conv_int] = participants
        if "is conversation starter?" in group.columns:
            starter_mask = group["is conversation starter?"].fillna(False).astype("bool")
            starter_rows = group[starter_mask]
        else:
            starter_rows = pd.DataFrame()
        starter_candidates = starter_rows["sender"].dropna().astype("string") if len(starter_rows) > 0 else pd.Series([], dtype="string")
        if len(starter_candidates) > 0:
            starter_by_conv[conv_int] = str(starter_candidates.iloc[0])
        else:
            starter_by_conv[conv_int] = str(senders.iloc[0])
    member_conversations = {}
    for conv_id, participants in participants_by_conv.items():
        for member in participants:
            member_conversations.setdefault(member, set()).add(conv_id)
    return participants_by_conv, starter_by_conv, member_conversations
