import React from "react";
import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";
import SelectMenu from "components/common/SelectMenu";

const MimeTypeForm = () => {
  const { mimeType, setMimeType } = useAnalysisForm(
    useShallow((s) => ({ mimeType: s.mimeType, setMimeType: s.setMimeType }))
  );

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
      <p className="text-sm text-slate-700 mb-1">File type:</p>
      <SelectMenu
        value={mimeType}
        onChange={(val) => setMimeType(val)}
        options={mimeTypes.map((m) => ({ value: m, label: m }))}
        placeholder="Select file type"
      />
    </div>
  );
};

export default MimeTypeForm;
