import { useEffect } from "react";
import { addArg, removeArg } from "../../utils";

const PhraseForm = ({ setFuncArgs }) => {
  useEffect(() => {
    addArg(setFuncArgs, "phrase", "");
  }, [setFuncArgs]);

  return (
    <div>
      <div className="input-div">
        <p>Phrase to search for:</p>
        <input
          type="text"
          onChange={(event) => addArg(setFuncArgs, "phrase", event.target.value)}
        />
      </div>
      <div className="input-div">
        <p>Search whole words (do not include results if phrase is within a larger word)?</p>
        <input
          type="checkbox"
          className="checkbox"
          onChange={(event) => {
            if (event.target.checked) {
              addArg(setFuncArgs, "separate", "");
            } else {
              removeArg(setFuncArgs, "separate");
            }
          }}
        />
      </div>
      <div className="input-div">
        <p>Case-sensitive search?</p>
        <input
          type="checkbox"
          className="checkbox"
          onChange={(event) => {
            if (event.target.checked) {
              addArg(setFuncArgs, "case-sensitive", "");
            } else {
              removeArg(setFuncArgs, "case-sensitive");
            }
          }}
        />
        <div className="sep-50"></div>
        <p>
          Use{" "}
          <a href="https://regexr.com/" target="_blank" rel="noreferrer">
            RegEx
          </a>
          ?
        </p>
        <input
          type="checkbox"
          className="checkbox"
          onChange={(event) => {
            if (event.target.checked) {
              addArg(setFuncArgs, "regex", "");
            } else {
              removeArg(setFuncArgs, "regex");
            }
          }}
        />
      </div>
    </div>
  );
};

export default PhraseForm;
