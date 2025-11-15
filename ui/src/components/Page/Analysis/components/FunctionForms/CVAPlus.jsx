import ConvoStarterForm from "./ConvoStarter";
import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";

const CVAPlusForm = ({ scope = "primary" }) => {
  const selectors = (s) => {
    if (scope === "scatter-x") {
      return {
        volumeWeight: s.scatterXCvaVolumeWeight,
        efficiencyWeight: s.scatterXCvaEfficiencyWeight,
        setVolumeWeight: s.setScatterXCvaVolumeWeight,
      };
    }
    if (scope === "scatter-y") {
      return {
        volumeWeight: s.scatterYCvaVolumeWeight,
        efficiencyWeight: s.scatterYCvaEfficiencyWeight,
        setVolumeWeight: s.setScatterYCvaVolumeWeight,
      };
    }
    return {
      volumeWeight: s.cvaVolumeWeight,
      efficiencyWeight: s.cvaEfficiencyWeight,
      setVolumeWeight: s.setCvaVolumeWeight,
    };
  };

  const { volumeWeight, efficiencyWeight, setVolumeWeight } = useAnalysisForm(useShallow(selectors));

  return (
    <div className="space-y-4">
      <ConvoStarterForm scope={scope} />
      <div className="input-div">
        <div className="flex justify-between text-sm text-slate-700 mb-2">
          <span>Volume weight: {Math.round(volumeWeight ?? 0)}%</span>
          <span>Efficiency weight: {Math.round(efficiencyWeight ?? 0)}%</span>
        </div>
        <input
          type="range"
          min="0"
          max="100"
          step="1"
          value={volumeWeight ?? 0}
          onChange={(e) => setVolumeWeight(e.target.valueAsNumber ?? 0)}
          className="w-full accent-slate-900"
        />
        <p className="text-xs text-slate-500 mt-1">
          Drag to balance volume metrics (messages sent, starters, participation, reactions sent/received) against efficiency metrics
          (weighted reactions per message, non-solo conversation rate). The weights always sum to 100%.
        </p>
      </div>
    </div>
  );
};

export default CVAPlusForm;
