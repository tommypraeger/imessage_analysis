import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";

const ReactionForm = () => {
  const { outputType, reactionType, setReactionType } = useAnalysisForm(
    useShallow((s) => ({
      outputType: s.outputType,
      reactionType: s.reactionType,
      setReactionType: s.setReactionType,
    }))
  );

  const reactionTypes = [
    { label: "All types (default)", value: "all" },
    { label: "Total (aggregate)", value: "total" },
    { label: "Love", value: "love" },
    { label: "Like", value: "like" },
    { label: "Dislike", value: "dislike" },
    { label: "Laugh", value: "laugh" },
    { label: "Emphasize", value: "emphasize" },
    { label: "Question", value: "question" },
    { label: "Custom Emoji", value: "custom emoji" },
  ];

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
