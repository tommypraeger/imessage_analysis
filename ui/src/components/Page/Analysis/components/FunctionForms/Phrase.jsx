import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";
import Tooltip from "components/common/Tooltip";

const PhraseForm = () => {
  const {
    phrase,
    setPhrase,
    phraseSeparate,
    setPhraseSeparate,
    phraseCaseSensitive,
    setPhraseCaseSensitive,
    phraseRegex,
    setPhraseRegex,
  } = useAnalysisForm(
    useShallow((s) => ({
      phrase: s.phrase,
      setPhrase: s.setPhrase,
      phraseSeparate: s.phraseSeparate,
      setPhraseSeparate: s.setPhraseSeparate,
      phraseCaseSensitive: s.phraseCaseSensitive,
      setPhraseCaseSensitive: s.setPhraseCaseSensitive,
      phraseRegex: s.phraseRegex,
      setPhraseRegex: s.setPhraseRegex,
    }))
  );

  return (
    <div>
      <div className="input-div">
        <p>Phrase to search for:</p>
        <input
          type="text"
          value={phrase}
          onChange={(e) => setPhrase(e.target.value)}
          className="border border-slate-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-300"
          placeholder="Enter a word or phrase"
        />
      </div>
      <div className="input-div flex items-center gap-3">
        <p className="m-0 flex items-center">
          Search whole words?
          <Tooltip text={"Only match whole tokens. Example: 'cat' will not match 'concatenate'."} />
        </p>
        <input type="checkbox" className="h-4 w-4 rounded accent-slate-900" checked={!!phraseSeparate} onChange={(e) => setPhraseSeparate(e.target.checked)} />
      </div>
      <div className="input-div flex items-center gap-3 mt-2">
        <p className="m-0">Case-sensitive search?</p>
        <input type="checkbox" className="h-4 w-4 rounded accent-slate-900" checked={!!phraseCaseSensitive} onChange={(e) => setPhraseCaseSensitive(e.target.checked)} />
        <div className="sep-50"></div>
        <p className="m-0">
          Use <a className="underline text-slate-700 hover:text-slate-900" href="https://regexr.com/" target="_blank" rel="noreferrer">RegEx</a>?
        </p>
        <input type="checkbox" className="h-4 w-4 rounded accent-slate-900" checked={!!phraseRegex} onChange={(e) => setPhraseRegex(e.target.checked)} />
      </div>
    </div>
  );
};

export default PhraseForm;
