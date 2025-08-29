import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";
import { REACTION_TYPE_OPTIONS } from "./common";
import SelectMenu from "components/common/SelectMenu";

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
      <p className="text-sm text-slate-700 mb-1">Reaction type (tables only):</p>
      <SelectMenu
        value={reactionType || "all"}
        onChange={(val) => setReactionType(val)}
        options={reactionTypes}
        placeholder="Select reaction type"
      />
    </div>
  );
};

export default ReactionForm;
