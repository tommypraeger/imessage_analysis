from analysis.functions.function import Function

# import all Function classes for __subclasses__() method
from analysis.functions.all_caps import AllCaps
from analysis.functions.attachment import Attachment
from analysis.functions.conversation_starter import ConversationStarter
from analysis.functions.emoji import Emoji
from analysis.functions.game import Game
from analysis.functions.link import Link
from analysis.functions.message_series import MessageSeries
from analysis.functions.mime_type import MimeType
from analysis.functions.participation import Participation
from analysis.functions.phrase import Phrase
from analysis.functions.reaction import Reaction
from analysis.functions.total import Total
from analysis.functions.tweet import Tweet
from analysis.functions.word_count import WordCount
from analysis.functions.word_length import WordLength


def get_function_class_by_name(function_name):
    return [
        function()
        for function in Function.__subclasses__()
        if function.get_function_name() == function_name
    ][0]
