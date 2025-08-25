import ConvoStarterForm from "./ConvoStarter";
import MessageSeriesForm from "./MessageSeries";
import MimeTypeForm from "./MimeType";
import ParticipationForm from "./Participation";
import PhraseForm from "./Phrase";
import ReactionForm from "./Reaction";
import ReactionsReceivedForm from "./ReactionsReceived";
import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";

const FunctionForm = () => {
  const { func } = useAnalysisForm(useShallow((s) => ({ func: s.func })));
  switch (func) {
    case "conversation_starter":
      return <ConvoStarterForm />;

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

    default:
      return null;
  }
};

export default FunctionForm;
