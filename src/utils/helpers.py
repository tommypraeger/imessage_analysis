import datetime
import json
import re
import string
import traceback

from typedstream.stream import TypedStreamReader

from src.utils import constants, sql

USERNAME = ""
CONTACT_IDS = ""
CHAT_IDS = ""


def initialize_member(member_name, result_dict):
    if member_name not in result_dict["names"]:
        result_dict["names"].append(member_name)


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
    # Keep only reaction rows, normalize reaction_to GUIDs
    mt = df["message_type"].astype("string")
    reactions = df[mt.isin(constants.REACTION_TYPES)].copy()
    reactions["reaction_to"] = reactions["reaction_to"].astype("string").str.replace(r"^p:0/", "", regex=True)

    # Count and collect tuples (user, reaction) per original message guid
    counts = reactions.groupby("reaction_to").size()
    tuples = reactions.groupby("reaction_to").apply(
        lambda g: list(zip(g["sender"].tolist(), g["message_type"].tolist()))
    )

    # Only original messages (not reactions)
    base = df[df["reaction_to"].isna()].copy()
    base["reaction_count"] = base["guid"].map(counts).fillna(0).astype("int64")
    _mapped = base["guid"].map(tuples)
    base["reactions_per_user"] = _mapped.apply(lambda x: x if isinstance(x, list) else [])
    return base
