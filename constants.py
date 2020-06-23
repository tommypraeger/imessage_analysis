from user_data import USERNAME, CHAT_IDS, CONTACT_ID_TO_NAME, CONTACT_NAME_TO_ID

TIME_OFFSET = 978307200000000000
CONVO_STARTER_THRESHOLD_MINUTES = 120
LINK_REGEX = ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]'
              '|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
FUNCTIONS = [
    'total',
    'reaction',
    'attachment',
    'emoji',
    'all caps',
    'tweet',
    'convo starter',
    'message word count',
    'word length',
    'link',
    'message series',
    'game'
]
GRAPH_OPTIONS = [
    'frequency'
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
