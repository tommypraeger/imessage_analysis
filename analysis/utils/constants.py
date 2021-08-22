import json

with open('./ui/public/user_data.json', 'r') as user_data_file:
    user_data = json.load(user_data_file)

USERNAME = user_data['username']
CONTACTS = user_data['contacts']
CHAT_IDS = user_data['chat_ids']
CONTACT_IDS = user_data['contact_ids']

MONTH = slice(0, 2)
DAY = slice(3, 5)
YEAR = slice(6, 10)
HOURS = slice(11, 13)
MINUTES = slice(14, 16)
SECONDS = slice(17, 19)

TIME_OFFSET = 978307200000000000
CONVERSATION_STARTER_THRESHOLD_MINUTES = 30
LINK_REGEX = (r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]'
              r'|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
FUNCTIONS_REGEX = (r'^([a-zA-Z][a-zA-Z0-9_]*).py')

GRAPH_COLORS = [
    'rgba(31, 120, 180, 1)',
    'rgba(51, 160, 44, 1)',
    'rgba(227, 26, 28, 1)',
    'rgba(255, 127, 0, 1)',
    'rgba(106, 61, 154, 1)',
    'rgba(177, 89, 40, 1)',
    'rgba(166, 206, 227, 1)',
    'rgba(178, 223, 138, 1)',
    'rgba(251, 154, 153, 1)',
    'rgba(253, 191, 111, 1)',
    'rgba(202, 178, 214, 1)',
    'rgba(255, 255, 153, 1)'
]

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
