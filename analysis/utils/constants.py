import json

with open('user_data.json', 'r') as user_data_file:
    user_data = json.load(user_data_file)

USERNAME = user_data['username']
CONTACTS = user_data['contacts']
CHAT_IDS = user_data['chat_ids']
CONTACT_IDS = user_data['contact_ids']

TIME_OFFSET = 978307200000000000
CONVO_STARTER_THRESHOLD_MINUTES = 30
LINK_REGEX = (r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]'
              r'|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
FUNCTIONS_REGEX = (r'^([a-zA-Z][a-zA-Z0-9_]*).py')
REACTIONS = [
    'Laughed at',
    'Emphasized',
    'Liked',
    'Disliked',
    'Questioned',
    'Loved',
    'Removed a like',
    'Removed a dislike',
    'Removed a heart',
    'Removed an exclamation',
    'Removed a question mark',
    'Removed a laugh'
]
GAMES = [
    '8 Ball',
    'Sea Battle',
    'Basketball',
    'Archery',
    'Anagrams',
    'Darts',
    'Cup Pong',
    'Mini Golf',
    'Knockout',
    'Crazy 8',
    'Four in a Row',
    'Paintball',
    'Word Hunt',
    'Shuffleboard',
    'Filler',
    'Tanks',
    'Checkers',
    'Chess',
    'Mancala',
    'Dots & Boxes',
    'Gomoku',
    'Reversi',
    '9 Ball',
    '20 Questions'
]
