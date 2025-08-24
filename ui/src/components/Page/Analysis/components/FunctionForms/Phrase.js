import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";

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
        <input type="text" value={phrase} onChange={(e) => setPhrase(e.target.value)} />
      </div>
      <div className="input-div">
        <p>Search whole words (do not include results if phrase is within a larger word)?</p>
        <input type="checkbox" className="checkbox" checked={!!phraseSeparate} onChange={(e) => setPhraseSeparate(e.target.checked)} />
      </div>
      <div className="input-div">
        <p>Case-sensitive search?</p>
        <input type="checkbox" className="checkbox" checked={!!phraseCaseSensitive} onChange={(e) => setPhraseCaseSensitive(e.target.checked)} />
        <div className="sep-50"></div>
        <p>
          Use{" "}
          <a href="https://regexr.com/" target="_blank" rel="noreferrer">
            RegEx
          </a>
          ?
        </p>
        <input type="checkbox" className="checkbox" checked={!!phraseRegex} onChange={(e) => setPhraseRegex(e.target.checked)} />
      </div>
    </div>
  );
};

export default PhraseForm;
