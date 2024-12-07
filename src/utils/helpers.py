import datetime
import emoji
import json
import math
import re
import string
import traceback

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

    return all_messages[all_messages.reaction_type == ""]


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


def convert_reaction(raw_reaction_type):
    raw_reaction_type = int(raw_reaction_type)
    return constants.REACTIONS.get(raw_reaction_type, "")


def is_reaction(reaction_type):
    # TODO: track the reactions each message gets
    reaction_type = str(reaction_type)
    return reaction_type != ""


def is_removed_reaction(reaction_type):
    reaction_type = str(reaction_type)
    return reaction_type.startswith("removed")


def is_attachment(msg, mime, reaction_type):
    return mime != "text/plain" and not is_game_message(msg, mime, reaction_type)


def is_phrase_in(phrase, msg, reaction_type, case_sensitive, separate, regex):
    if is_reaction(reaction_type):
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


def includes_emoji(msg, reaction_type):
    if is_reaction(reaction_type):
        return False
    msg = str(msg)
    return emoji.emoji_count(msg) > 0


def is_all_caps(msg):
    only_letters = re.compile("[^a-zA-Z]")
    msg = only_letters.sub("", str(msg))
    return len(msg) > 0 and msg == msg.upper()


def is_tweet(msg, reaction_type):
    if is_reaction(reaction_type):
        return False
    msg = str(msg)
    # not using regex for speed and because it's prob not necessary
    return "twitter.com" in msg and "status" in msg


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


def is_link(msg, reaction_type):
    if is_reaction(reaction_type):
        return False
    if re.match(constants.LINK_REGEX, str(msg)):
        return True
    return False


def is_game_message(msg, mime, reaction_type):
    if is_reaction(reaction_type):
        return False
    msg = str(msg)
    return (msg in constants.GAMES or msg == "�￼") and (
        mime == "image/jpeg" or mime == "image/heic"
    )


# unfortunately this is not accurate :/
# regular game messages also use "�￼" now
def _is_game_start(msg, mime, reaction_type):
    if is_reaction(reaction_type):
        return False
    return str(msg) == "�￼" and (mime == "image/jpeg" or mime == "image/heic")


def get_day(date):
    return f"{date.month}/{date.day}/{str(date.year)[-2:]}"


def get_week(date):
    last_monday = date - datetime.timedelta(days=date.weekday())
    return f"{last_monday.month}/{last_monday.day}/{str(last_monday.year)[-2:]}"


def get_month(date):
    return f"{date.month}/1/{str(date.year)[-2:]}"


def get_year(date):
    return f"1/1/{str(date.year)[-2:]}"
