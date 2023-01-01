import datetime
import emoji
import json
import os
import re
import string
import traceback
from statistics import mean

import analysis.utils.constants as constants
import analysis.utils.sql as sql


def get_functions():
    pattern = re.compile(constants.FUNCTIONS_REGEX)
    _, _, file_names = next(os.walk("./analysis/functions"))
    file_names = [
        pattern.match(file_name).group(1)
        for file_name in file_names
        if pattern.match(file_name)
    ]
    return file_names


def initialize_member(member_name, result_dict):
    if member_name not in result_dict["names"]:
        result_dict["names"].append(member_name)


def get_messages(df, member_name=None, time_period=None):
    condition = True
    if time_period is not None:
        condition = condition & (df["time_period"] == time_period)
    if member_name is not None:
        condition = condition & (df["sender"] == member_name)

    return df[condition]


def get_non_reaction_messages(df, member_name=None, time_period=None):
    all_messages = get_messages(df, member_name, time_period)

    return all_messages[~all_messages["is reaction?"]]


def get_total_messages(df, member_name=None, time_period=None):
    return len(get_messages(df, member_name, time_period))


def get_total_non_reaction_messages(df, member_name=None, time_period=None):
    return len(get_non_reaction_messages(df, member_name, time_period))


def contact_name_from_id(contact_id):
    for name in constants.CONTACT_IDS:
        if contact_id in constants.CONTACT_IDS[name]:
            return name
    return sql.get_phone_number_from_contact_id(contact_id)


def load_user_data():
    with open("./ui/public/user_data.json", "r") as user_data_file:
        user_data = json.load(user_data_file)
    return user_data


def save_user_data(user_data):
    with open("./ui/public/user_data.json", "w") as user_data_file:
        json.dump(user_data, user_data_file, indent=4)


def clean_phone_number(phone_number):
    digits = [i for i in phone_number if i.isdigit()]
    return "".join(digits)[-10:]


def make_error_message(msg):
    return {"errorMessage": f"{str(msg)}\n{traceback.format_exc()}"}


def make_success_message(msg):
    return {"successMessage": str(msg)}


def safe_divide(num, denom):
    try:
        return num / denom
    except ZeroDivisionError:
        return 0


def date_to_time(date, time=False, end=False):
    month = int(date[constants.MONTH])
    day = int(date[constants.DAY])
    year = int(date[constants.YEAR])

    if time:
        hours = int(date[constants.HOURS])
        minutes = int(date[constants.MINUTES])
        seconds = int(date[constants.SECONDS])
        timestamp = datetime.datetime(
            year, month, day, hours, minutes, seconds
        ).timestamp()
    else:
        if end:
            timestamp = datetime.datetime(year, month, day, 23, 59, 59).timestamp()
        else:
            timestamp = datetime.datetime(year, month, day).timestamp()

    return timestamp * 1e9


def is_reaction(msg):
    msg = str(msg)
    for reaction in constants.REACTIONS:
        if msg.startswith(reaction):
            return True
    return False


def reaction_action(msg):
    msg = str(msg)
    for reaction in constants.REACTIONS[:6]:
        if msg.startswith(reaction):
            return 1
    for reaction in constants.REACTIONS[6:]:
        if msg.startswith(reaction):
            return -1
    return 0


def like_react_action(msg):
    msg = str(msg)
    if msg.startswith("Liked"):
        return 1
    elif msg.startswith("Removed a like"):
        return -1
    return 0


def love_react_action(msg):
    msg = str(msg)
    if msg.startswith("Loved"):
        return 1
    elif msg.startswith("Removed a heart"):
        return -1
    return 0


def dislike_react_action(msg):
    msg = str(msg)
    if msg.startswith("Disliked"):
        return 1
    elif msg.startswith("Removed a dislike"):
        return -1
    return 0


def laugh_react_action(msg):
    msg = str(msg)
    if msg.startswith("Laughed"):
        return 1
    elif msg.startswith("Removed a laugh"):
        return -1
    return 0


def emphasis_react_action(msg):
    msg = str(msg)
    if msg.startswith("Emphasized"):
        return 1
    elif msg.startswith("Removed an emphasis"):
        return -1
    return 0


def question_react_action(msg):
    msg = str(msg)
    if msg.startswith("Questioned"):
        return 1
    elif msg.startswith("Removed a question mark"):
        return -1
    return 0


def is_not_reaction(msg):
    return not is_reaction(msg)


def is_attachment(mime):
    return mime != "text/plain"


def is_phrase_in(phrase, msg, case_sensitive, separate, regex):
    if is_reaction(msg):
        return False
    msg = str(msg)
    if regex:
        if re.match(phrase, msg):
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


def includes_emoji(msg):
    if is_reaction(msg):
        return False
    msg = str(msg)
    return emoji.emoji_count(msg) > 0


def is_all_caps(msg):
    only_letters = re.compile("[^a-zA-Z]")
    msg = only_letters.sub("", str(msg))
    return len(msg) > 0 and msg == msg.upper()


def is_tweet(msg):
    if is_reaction(msg):
        return False
    msg = str(msg)
    return "twitter.com" in msg


def is_conversation_starter(time_diff, threshold):
    if threshold is None:
        threshold = constants.CONVERSATION_STARTER_THRESHOLD_MINUTES
    return time_diff.total_seconds() > (threshold * 60)


def message_word_count(msg):
    return len(str(msg).split())


def message_letter_count(msg):
    msg = str(msg)
    return len(re.sub("[^a-zA-Z]+", "", msg))


def is_link(msg):
    if is_reaction(msg):
        return False
    if re.match(constants.LINK_REGEX, str(msg)):
        return True
    return False


def is_game_message(msg, mime):
    if is_reaction(msg):
        return False
    return (
        str(msg) in constants.GAMES
        and (mime == "image/jpeg" or mime == "image/heic")
        or is_game_start(msg, mime)
    )


def is_game_start(msg, mime):
    if is_reaction(msg):
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
