import AllCapsForm from "./AllCaps";
import AttachmentForm from "./Attachment";
import ConvoStarterForm from "./ConvoStarter";
import EmojiForm from "./Emoji";
import GameForm from "./Game";
import LinkForm from "./Link";
import MessageSeriesForm from "./MessageSeries";
import MimeTypeForm from "./MimeType";
import ParticipationForm from "./Participation";
import PhraseForm from "./Phrase";
import ReactionForm from "./Reaction";
import ReactionsReceivedForm from "./ReactionsReceived";
import TotalForm from "./Total";
import TweetForm from "./Tweet";
import WordCountForm from "./WordCount";
import WordLengthForm from "./WordLength";

const FunctionForm = ({ func, setFuncArgs, outputType, reactionType, setReactionType }) => {
  switch (func) {
    case "all_caps":
      return <AllCapsForm />;

    case "attachment":
      return <AttachmentForm />;

    case "conversation_starter":
      return <ConvoStarterForm setFuncArgs={setFuncArgs} />;

    case "emoji":
      return <EmojiForm />;

    case "game":
      return <GameForm />;

    case "link":
      return <LinkForm />;

    case "message_series":
      return <MessageSeriesForm setFuncArgs={setFuncArgs} />;

    case "mime_type":
      return <MimeTypeForm setFuncArgs={setFuncArgs} />;

    case "participation":
      return <ParticipationForm setFuncArgs={setFuncArgs} />;

    case "phrase":
      return <PhraseForm setFuncArgs={setFuncArgs} />;

    case "reaction":
      return (
        <ReactionForm outputType={outputType} reactionType={reactionType} setReactionType={setReactionType} />
      );

    case "reactions_received":
      return (
        <ReactionsReceivedForm
          outputType={outputType}
          reactionType={reactionType}
          setReactionType={setReactionType}
        />
      );

    case "total":
      return <TotalForm />;

    case "tweet":
      return <TweetForm />;

    case "word_count":
      return <WordCountForm />;

    case "word_length":
      return <WordLengthForm />;

    default:
      return <TotalForm />;
  }
};

export default FunctionForm;
