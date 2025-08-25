import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";
import { REACTION_TYPE_OPTIONS } from "./common";

const ReactionForm = () => {
  const { outputType, reactionType, setReactionType } = useAnalysisForm(
    useShallow((s) => ({
      outputType: s.outputType,
      reactionType: s.reactionType,
      setReactionType: s.setReactionType,
    }))
  );

  const reactionTypes = REACTION_TYPE_OPTIONS;

  if (outputType !== "table") {
    return <div />;
  }

  return (
    <div className="input-div">
      <p>Reaction type (tables only):</p>
      <select
        className="select"
        value={reactionType || "all"}
        onChange={(event) => setReactionType(event.target.value)}
      >
        {reactionTypes.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default ReactionForm;
