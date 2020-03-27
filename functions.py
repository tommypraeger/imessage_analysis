import datetime
import re
import string
from statistics import mean

from emoji import UNICODE_EMOJI

from constants import *


# Filter by from date and to date
def date_to_time(date, end=False):
    month = int(date[0:2])
    day = int(date[2:4])
    year = int(date[4:6])
    if end:
        timestamp = datetime.datetime(2000 + year, month, day, 23, 59, 59).timestamp()
    else:
        timestamp = datetime.datetime(2000 + year, month, day).timestamp()
    return timestamp * 1e9 - TIME_OFFSET


def is_reaction(msg):
    msg = str(msg)
    for reaction in REACTIONS:
        if msg.startswith(reaction):
            return True
    return False


def reaction_action(msg):
    msg = str(msg)
    for reaction in REACTIONS[:6]:
        if msg.startswith(reaction):
            return 1
    for reaction in REACTIONS[6:]:
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


def is_convo_starter(time_diff):
    return time_diff.total_seconds() > CONVO_STARTER_THRESHOLD_MINUTES * 60


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
    if re.match(LINK_REGEX, str(msg)):
        return True
    return False


def is_game_message(msg, mime):
    if is_reaction(msg):
        return False
    return str(msg) in GAMES and mime == 'image/jpeg' or is_game_start(msg, mime)


def is_game_start(msg, mime):
    if is_reaction(msg):
        return False
    return str(msg) == '�￼' and mime == 'image/jpeg'
