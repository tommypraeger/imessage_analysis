// Centralized list of analysis function options
// Includes a supportsScatter flag to indicate compatibility with scatter plots

export const FUNCTION_OPTIONS = [
  { value: "total", label: "Total", desc: "How many messages each person sends", supportsScatter: true },
  { value: "reaction", label: "Reactions sent", desc: "How many iMessage reactions each person sends", supportsScatter: true },
  { value: "reactions_received", label: "Reactions received", desc: "How many iMessage reactions each person receives", supportsScatter: true },
  { value: "reaction_matrix", label: "Reaction matrix", desc: "How many reactions each person receives from each other person", supportsScatter: false },
  { value: "participation", label: "Participation", desc: "How often each person participates", supportsScatter: true },
  { value: "conversation_starter", label: "Starters", desc: "How many times each person starts the conversation", supportsScatter: true },
  { value: "phrase", label: "Word/Phrase", desc: "How many messages include a certain word/phrase", supportsScatter: true },
  { value: "message_series", label: "Message Series", desc: "How many series of consecutive messages each person sends", supportsScatter: true },
  { value: "word_count", label: "Word Count", desc: "Average word count per message", supportsScatter: true },
  { value: "word_length", label: "Word Length", desc: "Average length of each word sent", supportsScatter: true },
  { value: "attachment", label: "Attachments", desc: "How many messages are attachments", supportsScatter: true },
  { value: "link", label: "Links", desc: "How many messages are links", supportsScatter: true },
  { value: "emoji", label: "Emoji", desc: "How many messages include emoji", supportsScatter: true },
  { value: "game", label: "Games", desc: "How many messages are iMessage games", supportsScatter: true },
  { value: "tweet", label: "Tweets", desc: "How many messages are tweets", supportsScatter: true },
  { value: "all_caps", label: "All Caps", desc: "How many messages are in all caps", supportsScatter: true },
  { value: "mime_type", label: "File Type", desc: "How many messages are of a specific file type", supportsScatter: true },
];

export const getFunctionOptions = (opts = {}) => {
  const { forScatter = false } = opts;
  if (!forScatter) return FUNCTION_OPTIONS;
  return FUNCTION_OPTIONS.filter((o) => o.supportsScatter);
};

