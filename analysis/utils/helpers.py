import datetime
import os
import re
import string
from statistics import mean
from dateutil import relativedelta

from emoji import UNICODE_EMOJI

import analysis.utils.constants as constants


def get_functions():
    pattern = re.compile(constants.FUNCTIONS_REGEX)
    _, _, file_names = next(os.walk('./analysis/functions'))
    file_names = [
        pattern.match(file_name).group(1) for file_name in file_names 
        if pattern.match(file_name)
    ]
    return file_names


def contact_name_from_id(contact_id):
    for name in constants.CONTACT_IDS:
        if contact_id in constants.CONTACT_IDS[name]:
            return name


def date_to_time(date, end=False):
    month = int(date[0:2])
    day = int(date[2:4])
    year = int(date[4:6])
    if end:
        timestamp = datetime.datetime(2000 + year, month, day, 23, 59, 59).timestamp()
    else:
        timestamp = datetime.datetime(2000 + year, month, day).timestamp()
    return timestamp * 1e9 - constants.TIME_OFFSET


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
    if msg.startswith('Liked'):
        return 1
    elif msg.startswith('Removed a like'):
        return -1
    return 0


def love_react_action(msg):
    msg = str(msg)
    if msg.startswith('Loved'):
        return 1
    elif msg.startswith('Removed a heart'):
        return -1
    return 0


def dislike_react_action(msg):
    msg = str(msg)
    if msg.startswith('Disliked'):
        return 1
    elif msg.startswith('Removed a dislike'):
        return -1
    return 0


def laugh_react_action(msg):
    msg = str(msg)
    if msg.startswith('Laughed'):
        return 1
    elif msg.startswith('Removed a laugh'):
        return -1
    return 0


def emphasis_react_action(msg):
    msg = str(msg)
    if msg.startswith('Emphasized'):
        return 1
    elif msg.startswith('Removed an emphasis'):
        return -1
    return 0


def question_react_action(msg):
    msg = str(msg)
    if msg.startswith('Questioned'):
        return 1
    elif msg.startswith('Removed a question mark'):
        return -1
    return 0


def is_not_reaction(msg):
    return not is_reaction(msg)


def is_attachment(mime):
    return mime != 'text/plain'


def is_phrase_in(phrase, msg, case_sensitive, separate):
    if is_reaction(msg):
        return False
    msg = str(msg)
    if not case_sensitive:
        msg = msg.lower()
        phrase = phrase.lower()
    if separate:
        msg = msg.translate(str.maketrans('', '', string.punctuation)).split()
        phrase = phrase.split()
        return is_sub_list(phrase, msg)
    else:
        return phrase in msg


def is_sub_list(small, big):
    if len(small) > len(big):
        return False
    small_length = len(small)
    for i in range(len(big) - small_length + 1):
        if big[i:i + small_length] == small:
            return True
    return False


def is_type(test, target):
    return str(test) == target


def includes_emoji(msg):
    if is_reaction(msg):
        return False
    msg = str(msg)
    for emoji in UNICODE_EMOJI:
        if emoji in msg:
            return True
    return False


def is_all_caps(msg):
    only_letters = re.compile('[^a-zA-Z]')
    msg = only_letters.sub('', str(msg))
    not_all_emojis = False
    for c in msg:
        if c not in UNICODE_EMOJI:
            not_all_emojis = True
    return not_all_emojis and len(msg) > 0 and msg == msg.upper()


def is_tweet(msg):
    if is_reaction(msg):
        return False
    msg = str(msg)
    return 'twitter.com' in msg


def is_convo_starter(time_diff, threshold):
    if threshold is None:
        threshold = constants.CONVO_STARTER_THRESHOLD_MINUTES
    return time_diff.total_seconds() > (threshold * 60)


def message_word_count(msg):
    return len(str(msg).split())


def average_word_length(msg):
    msg = str(msg)
    msg = msg.translate(str.maketrans('', '', string.punctuation)).split()
    if len(msg) == 0:
        return 0
    return mean([len(word) for word in msg])


def is_link(msg):
    if is_reaction(msg):
        return False
    if re.match(constants.LINK_REGEX, str(msg)):
        return True
    return False


def is_game_message(msg, mime):
    if is_reaction(msg):
        return False
    return str(msg) in constants.GAMES and mime == 'image/jpeg' or is_game_start(msg, mime)


def is_game_start(msg, mime):
    if is_reaction(msg):
        return False
    return str(msg) == '�￼' and mime == 'image/jpeg'


def get_day(date):
    return f'{date.month}/{date.day}/{str(date.year)[-2:]}'


def get_week(date):
    last_monday = date - datetime.timedelta(days=date.weekday())
    return f'{last_monday.month}/{last_monday.day}/{str(last_monday.year)[-2:]}'

def get_month(date):
    return f'{date.month}/1/{str(date.year)[-2:]}'


def get_year(date):
    return f'1/1/{str(date.year)[-2:]}'


def get_time_periods(begin_date, end_date, time_period_name):
    if time_period_name == 'day':
        num_days = (end_date - begin_date).days
        return [
            get_day(begin_date + relativedelta.relativedelta(days=i))
            for i in range(num_days + 1)
        ]
    if time_period_name == 'week':
        num_weeks = (end_date - begin_date).days // 7
        return [
            get_week(begin_date + relativedelta.relativedelta(days=i*7))
            for i in range(num_weeks + 1)
        ]
    if time_period_name == 'month':
        num_months = (end_date.year - begin_date.year) * 12 + (end_date.month - begin_date.month)
        return [
            get_month(begin_date + relativedelta.relativedelta(months=i))
            for i in range(num_months + 1)
        ]
    if time_period_name == 'year':
        num_years = end_date.year - begin_date.year
        return [
            get_year(begin_date + relativedelta.relativedelta(years=i))
            for i in range(num_years + 1)
        ]
