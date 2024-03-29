import React, { useEffect } from "react";
import { addArg } from "../../utils";

const MessageSeriesForm = ({ setFuncArgs }) => {
  useEffect(() => {
    addArg(setFuncArgs, "minutes-threshold", 60);
  }, [setFuncArgs]);

  return (
    <div className="input-div">
      <p>
        Time (in minutes) after the previous message for a new message to be classified as a new
        conversation:
      </p>
      <input
        type="number"
        min="1"
        defaultValue="60"
        onChange={(event) => addArg(setFuncArgs, "minutes-threshold", event.target.valueAsNumber)}
      />
    </div>
  );
};

export default MessageSeriesForm;
