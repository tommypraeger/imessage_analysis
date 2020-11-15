import AllFunctionsForm from './AllFunctions';
import AllCapsForm from './AllCaps';
import AttachmentForm from './Attachment';
import ConvoStarterForm from './ConvoStarter';
import EmojiForm from './Emoji';
import FrequencyForm from './Frequency';
import GameForm from './Game';
import LinkForm from './Link';
import MessageSeriesForm from './MessageSeries';
import MimeTypeForm from './MimeType';
import PhraseForm from './Phrase';
import ReactionForm from './Reaction';
import TotalForm from './Total';
import TweetForm from './Tweet';
import WordCountForm from './WordCount';
import WordLengthForm from './WordLength';

const FunctionForm = ({ func }) => {
  switch (func) {
    case 'all_functions':
      return <AllFunctionsForm />

    case 'all_caps':
      return <AllCapsForm />;

    case 'attachment':
      return <AttachmentForm />;

    case 'convo_start':
      return <ConvoStarterForm />;

    case 'emoji':
      return <EmojiForm />;

    case 'frequency':
      return <FrequencyForm />;

    case 'game':
      return <GameForm />;

    case 'link':
      return <LinkForm />;

    case 'message_series':
      return <MessageSeriesForm />;

    case 'mime_type':
      return <MimeTypeForm />;

    case 'phrase':
      return <PhraseForm />;

    case 'reaction':
      return <ReactionForm />;

    case 'total':
      return <TotalForm />;

    case 'tweet':
      return <TweetForm />;

    case 'word_count':
      return <WordCountForm />;

    case 'word_length':
      return <WordLengthForm />;

    default:
      return <TotalForm />;
  };
};

export default FunctionForm;
