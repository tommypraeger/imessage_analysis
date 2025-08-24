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
import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";
import TotalForm from "./Total";
import TweetForm from "./Tweet";
import WordCountForm from "./WordCount";
import WordLengthForm from "./WordLength";

const FunctionForm = () => {
  const { func } = useAnalysisForm(useShallow((s) => ({ func: s.func })));
  switch (func) {
    case "all_caps":
      return <AllCapsForm />;

    case "attachment":
      return <AttachmentForm />;

    case "conversation_starter":
      return <ConvoStarterForm />;

    case "emoji":
      return <EmojiForm />;

    case "game":
      return <GameForm />;

    case "link":
      return <LinkForm />;

    case "message_series":
      return <MessageSeriesForm />;

    case "mime_type":
      return <MimeTypeForm />;

    case "participation":
      return <ParticipationForm />;

    case "phrase":
      return <PhraseForm />;

    case "reaction":
      return <ReactionForm />;

    case "reactions_received":
      return <ReactionsReceivedForm />;

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
