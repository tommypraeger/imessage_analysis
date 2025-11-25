import ConvoStarterForm from "./ConvoStarter";
import MessageSeriesForm from "./MessageSeries";
import MimeTypeForm from "./MimeType";
import ParticipationForm from "./Participation";
import PhraseForm from "./Phrase";
import ReactionForm from "./Reaction";
import ReactionsReceivedForm from "./ReactionsReceived";
import CVAPlusForm from "./CVAPlus";
import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";

const FunctionForm = ({ func: overrideFunc, scope = "primary" }) => {
  const { func } = useAnalysisForm(useShallow((s) => ({ func: s.func })));
  const activeFunc = overrideFunc || func;
  switch (activeFunc) {
    case "conversation_starter":
      return <ConvoStarterForm scope={scope} />;

    case "solo_conversations":
      return <ConvoStarterForm scope={scope} />;

    case "message_series":
      return <MessageSeriesForm scope={scope} />;

    case "mime_type":
      return <MimeTypeForm scope={scope} />;

    case "participation":
      return <ParticipationForm scope={scope} />;

    case "participation_correlation":
      return <ParticipationForm scope={scope} />;

    case "phrase":
      return <PhraseForm scope={scope} />;

    case "cva_plus":
      return <CVAPlusForm scope={scope} />;

    case "reaction":
      return <ReactionForm />;

    case "reactions_received":
      return <ReactionsReceivedForm />;

    default:
      return null;
  }
};

export default FunctionForm;
