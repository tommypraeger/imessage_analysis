import ast
import datetime
import emoji
import json
import math
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
    condition = df["text"].apply(is_not_edit)
    if time_period is not None:
        condition = condition & (df["time_period"] == time_period)
    if member_name is not None:
        condition = condition & (df["sender"] == member_name)

    return df[condition]


def get_non_reaction_messages(df, member_name=None, time_period=None):
    all_messages = get_messages(df, member_name, time_period)

    return all_messages[all_messages.message_type.apply(is_not_reaction)]


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
    return {"errorMessage": f"{str(msg)}\n{traceback.format_exc()}"}


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


# TODO: find way to link edits to the original message
# TODO: find better way to identify edits
def is_edit(msg):
    msg = str(msg)
    return msg.startswith("Edited to")


def is_not_edit(msg):
    return not is_edit(msg)


def convert_message_type(raw_message_type):
    raw_message_type = int(raw_message_type)
    return constants.MESSAGE_TYPES.get(raw_message_type, "")


def is_reaction(message_type):
    message_type = str(message_type)
    return message_type in constants.REACTION_TYPES


def is_removed_reaction(message_type):
    message_type = str(message_type)
    return message_type.startswith("removed")


def is_not_reaction(message_type):
    return not is_reaction(message_type) and not is_removed_reaction(message_type)


def is_attachment(msg, mime, message_type):
    return mime != "text/plain" and not is_game_message(message_type)


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


def is_type(test, target):
    return str(test) == target


def includes_emoji(msg, message_type):
    if is_reaction(message_type):
        return False
    msg = str(msg)
    return emoji.emoji_count(msg) > 0


def is_all_caps(msg):
    only_letters = re.compile("[^a-zA-Z]")
    msg = only_letters.sub("", str(msg))
    return len(msg) > 0 and msg == msg.upper()


def is_tweet(msg, message_type):
    if is_reaction(message_type):
        return False
    msg = str(msg)
    # not using regex for speed and because it's prob not necessary
    return (("/twitter.com" in msg
            or "/x.com" in msg) # 🤮
            and "status" in msg)


def is_conversation_starter(time_diff, threshold):
    if threshold is None:
        threshold = constants.DEFAULT_CONVERSATION_STARTER_THRESHOLD_MINUTES
    time_diff_in_seconds = time_diff.total_seconds()

    # shouldn't actually be necessary to check for nan
    # because I already set the first message as a conversation starter
    # but might as well
    return math.isnan(time_diff_in_seconds) or time_diff_in_seconds > (threshold * 60)


def message_word_count(msg):
    return len(str(msg).split())


def message_letter_count(msg):
    msg = str(msg)
    return len(re.sub("[^a-zA-Z]+", "", msg))


def is_link(msg, message_type):
    if is_reaction(message_type):
        return False
    if re.match(constants.LINK_REGEX, str(msg)):
        return True
    return False


def is_game_message(message_type):
    return message_type == "game" or message_type == "game start"


def is_game_start(message_type):
    return message_type == "game start"


def get_day(date):
    return f"{date.month}/{date.day}/{str(date.year)[-2:]}"


def get_week(date):
    last_monday = date - datetime.timedelta(days=date.weekday())
    return f"{last_monday.month}/{last_monday.day}/{str(last_monday.year)[-2:]}"


def get_month(date):
    return f"{date.month}/1/{str(date.year)[-2:]}"


def get_year(date):
    return f"1/1/{str(date.year)[-2:]}"


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
    # Filter rows with reactions
    reactions = df[df["message_type"].apply(is_reaction)].copy()

    # Clean the reaction_to column to match GUIDs
    reactions["reaction_to"] = reactions["reaction_to"].str.replace(r"^p:0/", "", regex=True)

    # Group reactions by the original message GUID
    reactions_grouped = reactions.groupby("reaction_to").agg({
        "message_type": lambda x: list(x),  # Collect all reaction types
        "sender": lambda x: list(x)  # Collect all users who reacted
    }).rename(columns={"message_type": "reactions", "sender": "reacting_users"})

    # Merge the grouped reactions back into the original dataframe
    df = df.merge(
        reactions_grouped,
        how="left",
        left_on="guid",
        right_index=True
    )

    # Fill NaN for messages with no reactions
    df["reactions"] = df["reactions"].apply(lambda x: x if isinstance(x, list) else [])
    df["reacting_users"] = df["reacting_users"].apply(lambda x: x if isinstance(x, list) else [])

    # Safely parse the reactions and reacting_users columns using ast.literal_eval
    df["reaction_count"] = df["reactions"].apply(
        lambda x: len(ast.literal_eval(str(x))) if x else 0
    )

    # Filter for rows that are messages (not reactions)
    df = df[df["reaction_to"].isna()]

    # Add a column for the total reactions each sender has received
    df["total_reactions_received"] = df.groupby("reaction_to")["reaction_count"].transform("sum")

    # Extract reaction types per user from the 'reactions' column
    df["reactions_per_user"] = df.apply(
        lambda row: list(zip(ast.literal_eval(str(row["reacting_users"])), ast.literal_eval(str(row["reactions"]))))
        if row["reactions"] else [],
        axis=1
    )
    del df["reactions"]
    del df["reacting_users"]

    return df
