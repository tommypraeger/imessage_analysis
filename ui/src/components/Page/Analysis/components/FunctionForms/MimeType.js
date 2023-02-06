import React, { useEffect } from "react";
import { addArg } from "../../utils";

const MimeTypeForm = ({ setFuncArgs }) => {
  useEffect(() => {
    addArg(setFuncArgs, "mime-type", "image/png");
  }, [setFuncArgs]);

  const mimeTypes = [
    "image/png",
    "image/jpeg",
    "image/gif",
    "image/heic",
    "video/mp4",
    "video/quicktime",
    "text/plain",
    "text/markdown",
    "text/csv",
    "text/vcard",
    "audio/mpeg",
    "audio/amr",
    "audio/x-m4a",
    "text/x-python-script",
    "text/x-vlocation",
    "text/html",
    "text/css",
    "application/pdf",
    "application/json",
    "application/x-tex",
    "application/x-javascript",
    "application/x-iwork-keynote-sffkey",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/zip",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel",
    "application/epub+zip",
    "application/x-yaml",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "message/rfc822",
  ];

  return (
    <div className="input-div">
      <p>File type:</p>
      <select
        className="select"
        defaultValue="image/png"
        onChange={(event) => addArg(setFuncArgs, "mime-type", event.target.value)}
      >
        {mimeTypes.map((mimeType) => (
          <option key={mimeType} value={mimeType}>
            {mimeType}
          </option>
        ))}
      </select>
    </div>
  );
};

export default MimeTypeForm;
