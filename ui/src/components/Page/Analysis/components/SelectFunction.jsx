import { useEffect } from "react";
import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";
import useAnalysisRunner from "../useAnalysisRunner";
import SelectMenu from "components/common/SelectMenu";

const SelectFunction = () => {
  const { outputType, func, setFunc, setCategory, graphIndividual } = useAnalysisForm(
    useShallow((s) => ({
      outputType: s.outputType,
      func: s.func,
      setFunc: s.setFunc,
      setCategory: s.setCategory,
      graphIndividual: s.graphIndividual,
    }))
  );
  const { fetchCategories } = useAnalysisRunner();

  // Default to 'total' if no function selected yet
  useEffect(() => {
    if (!func) {
      setFunc("total");
      setCategory("");
      fetchCategories("total", outputType, graphIndividual);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const options = [
    { value: "total", label: "Total", desc: "How many messages each person sends" },
    { value: "reaction", label: "Reactions sent", desc: "How many iMessage reactions each person sends" },
    { value: "reactions_received", label: "Reactions received", desc: "How many iMessage reactions each person receives" },
    { value: "reaction_matrix", label: "Reaction matrix", desc: "How many reactions each person receives from each other person" },
    { value: "participation", label: "Participation", desc: "How often each person participates" },
    { value: "conversation_starter", label: "Starters", desc: "How many times each person starts the conversation" },
    { value: "phrase", label: "Word/Phrase", desc: "How many messages include a certain word/phrase" },
    { value: "message_series", label: "Message Series", desc: "How many series of consecutive messages each person sends" },
    { value: "word_count", label: "Word Count", desc: "Average word count per message" },
    { value: "word_length", label: "Word Length", desc: "Average length of each word sent" },
    { value: "attachment", label: "Attachments", desc: "How many messages are attachments" },
    { value: "link", label: "Links", desc: "How many messages are links" },
    { value: "emoji", label: "Emoji", desc: "How many messages include emoji" },
    { value: "game", label: "Games", desc: "How many messages are iMessage games" },
    { value: "tweet", label: "Tweets", desc: "How many messages are tweets" },
    { value: "all_caps", label: "All Caps", desc: "How many messages are in all caps" },
    { value: "mime_type", label: "File Type", desc: "How many messages are of a specific file type" },
  ];

  return (
    <div>
      <h2 className="text-sm font-medium text-slate-700 mb-1">Function:</h2>
      <SelectMenu
        value={func || "total"}
        onChange={(val) => {
          setFunc(val);
          setCategory("");
          fetchCategories(val, outputType, graphIndividual);
        }}
        options={options}
        placeholder="Select function"
      />
    </div>
  );
};

export default SelectFunction;
