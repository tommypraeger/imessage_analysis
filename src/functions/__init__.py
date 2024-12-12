from src.functions.function import Function

# import all Function classes for __subclasses__() method
from src.functions.definitions.all_caps import AllCaps
from src.functions.definitions.attachment import Attachment
from src.functions.definitions.conversation_starter import ConversationStarter
from src.functions.definitions.emoji import Emoji
from src.functions.definitions.game import Game
from src.functions.definitions.link import Link
from src.functions.definitions.message_series import MessageSeries
from src.functions.definitions.mime_type import MimeType
from src.functions.definitions.participation import Participation
from src.functions.definitions.phrase import Phrase
from src.functions.definitions.reaction import Reaction
from src.functions.definitions.reactions_received import ReactionsReceived
from src.functions.definitions.reaction_matrix import ReactionMatrix
from src.functions.definitions.total import Total
from src.functions.definitions.tweet import Tweet
from src.functions.definitions.word_count import WordCount
from src.functions.definitions.word_length import WordLength

def get_function_class_by_name(function_name):
    return [
        function()
        for function in Function.__subclasses__()
        if function.get_function_name() == function_name
    ][0]


def get_functions():
    return [f.get_function_name() for f in Function.__subclasses__()]
