USER_DATA_FILE_NAME = "user_data.json"

DATE_FORMATS = [
    "%Y-%m-%d",
    "%Y-%m-%d %H:%M:%S",
    "%m/%d/%Y",
    "%m/%d/%Y %H:%M:%S",
]

TIME_OFFSET = 978307200000000000
DEFAULT_CONVERSATION_STARTER_THRESHOLD_MINUTES = 30
LINK_REGEX = (
    r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]"
    r"|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)

GRAPH_COLORS = [
    "rgba(31, 120, 180, 1)",
    "rgba(51, 160, 44, 1)",
    "rgba(227, 26, 28, 1)",
    "rgba(255, 127, 0, 1)",
    "rgba(106, 61, 154, 1)",
    "rgba(177, 89, 40, 1)",
    "rgba(166, 206, 227, 1)",
    "rgba(178, 223, 138, 1)",
    "rgba(251, 154, 153, 1)",
    "rgba(253, 191, 111, 1)",
    "rgba(202, 178, 214, 1)",
    "rgba(255, 255, 153, 1)",
]
GRAPH_TOTAL_KEY = "Total"

REACTIONS = {
    2000: "love",
    2001: "like",
    2002: "dislike",
    2003: "laugh",
    2004: "emphasize",
    2005: "question",
    3000: "removed love",
    3001: "removed like",
    3002: "removed dislike",
    3003: "removed laugh",
    3004: "removed emphasize",
    3005: "removed question"
}
GAMES = [
    "8 Ball",
    "Sea Battle",
    "Basketball",
    "Archery",
    "Anagrams",
    "Darts",
    "Cup Pong",
    "Mini Golf",
    "Knockout",
    "Crazy 8",
    "Four in a Row",
    "Paintball",
    "Word Hunt",
    "Shuffleboard",
    "Filler",
    "Tanks",
    "Checkers",
    "Chess",
    "Mancala",
    "Dots & Boxes",
    "Gomoku",
    "Reversi",
    "9 Ball",
    "20 Questions",
]
