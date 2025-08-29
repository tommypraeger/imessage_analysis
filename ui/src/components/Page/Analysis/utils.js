import $ from "jquery";
import "datatables.net";
import "datatables.net-dt/css/jquery.dataTables.css";
import { postFetch } from "../utils";
import useAnalysisForm from "state/analysisStore";

// Map UI reaction type values to column labels for table hiding
const REACTION_PER_TYPE_COLUMNS = {
  reaction: {
    like: ["Like reacts", "Percent of reactions that are Like reacts"],
    love: ["Love reacts", "Percent of reactions that are Love reacts"],
    dislike: ["Dislike reacts", "Percent of reactions that are Dislike reacts"],
    laugh: ["Laugh reacts", "Percent of reactions that are Laugh reacts"],
    emphasize: ["Emphasize reacts", "Percent of reactions that are Emphasize reacts"],
    question: ["Question reacts", "Percent of reactions that are Question reacts"],
    "custom emoji": [
      "Custom Emoji reacts",
      "Percent of reactions that are Custom Emoji reacts",
    ],
  },
  reactions_received: {
    like: ["Like reacts received", "Like reacts received per message"],
    love: ["Love reacts received", "Love reacts received per message"],
    dislike: ["Dislike reacts received", "Dislike reacts received per message"],
    laugh: ["Laugh reacts received", "Laugh reacts received per message"],
    emphasize: ["Emphasize reacts received", "Emphasize reacts received per message"],
    question: ["Question reacts received", "Question reacts received per message"],
    "custom emoji": [
      "Custom Emoji reacts received",
      "Custom Emoji reacts received per message",
    ],
  },
};

const formatDate = (date) => {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
};

const buildArgs = () => {
  const s = useAnalysisForm.getState();
  const {
    contactName,
    func,
    outputType,
    category,
    group,
    csv,
    csvFileName,
    startDate,
    endDate,
  } = s;

  const args = { name: contactName, export: "" };
  args.function = func;

  // Function-specific transient args composed from store
  if (func === "phrase") {
    args["phrase"] = s.phrase || "";
    if (s.phraseSeparate) args["separate"] = "";
    if (s.phraseCaseSensitive) args["case-sensitive"] = "";
    if (s.phraseRegex) args["regex"] = "";
  }
  if (func === "mime_type") {
    args["mime-type"] = s.mimeType;
  }
  if (func === "message_series" || func === "conversation_starter" || func === "participation") {
    if (typeof s.minutesThreshold === "number" && !Number.isNaN(s.minutesThreshold)) {
      args["minutes-threshold"] = s.minutesThreshold;
    }
  }

  // Output + graph-specific args
  args[outputType] = "";
  if (outputType === "graph") {
    if (s.graphIndividual) args["graph-individual"] = "";
    if (s.graphTimeInterval) args["graph-time-interval"] = s.graphTimeInterval;
  }

  if (category) args.category = category;

  // group and csv shouldn't be set at the same time (group has priority)
  if (group) {
    args.group = "";
  } else if (csv) {
    args.csv = "";
    args["csv-file-path"] = csvFileName;
  }

  if (startDate) args["from-date"] = formatDate(startDate);
  if (endDate) args["to-date"] = formatDate(endDate);

  return args;
};

const runAnalysis = (setFetchesInProgress, setResponse) => {
  setResponse({});
  const s = useAnalysisForm.getState();
  const args = buildArgs();
  postFetch("analysis", args, setFetchesInProgress)
    .then((response) => {
      // If we received an HTML table, optionally strip irrelevant columns
      if (response && response.htmlTable) {
        response = Object.assign({}, response, {
          htmlTable: filterHtmlTableByReactionType(s.func, s.reactionType, response.htmlTable),
        });
      }
      setResponse(response);
    })
    .catch((err) => console.log(err))
    .finally(() => setFetchesInProgress((fetches) => fetches - 1));
};

const makeTableNice = () => {
  const $table = $("#analysis-table").children("table");
  if ($table.length === 0) return;

  // Enhance with DataTables
  $table.DataTable({
    paging: false,
    searching: false,
  });
};

// Remove columns from a Pandas HTML table output matching reactionType selection
const filterHtmlTableByReactionType = (func, reactionType, html) => {
  try {
    if (!html || !reactionType || reactionType === "all") return html;
    if (!(func === "reaction" || func === "reactions_received")) return html;

    const perTypeMap = REACTION_PER_TYPE_COLUMNS[func] || {};
    const allPerTypeHeaders = Object.values(perTypeMap).flat();
    if (allPerTypeHeaders.length === 0) return html;

    const container = document.createElement("div");
    container.innerHTML = html;
    const table = container.querySelector("table");
    if (!table) return html;

    const headerRow = table.querySelector("tr");
    if (!headerRow) return html;
    const ths = Array.from(headerRow.querySelectorAll("th"));

    // Compute indices to remove based on selection
    let indicesToRemove = [];
    if (reactionType === "total") {
      // Remove only per-type columns; keep aggregates and names
      ths.forEach((th, i) => {
        const text = (th.textContent || "").trim();
        if (allPerTypeHeaders.includes(text)) {
          indicesToRemove.push(i);
        }
      });
    } else if (reactionType in perTypeMap) {
      // Keep only the chosen per-type columns (plus first column which is names)
      const keepHeaders = new Set(perTypeMap[reactionType]);
      ths.forEach((th, i) => {
        if (i === 0) return; // always keep first column (names)
        const text = (th.textContent || "").trim();
        if (!keepHeaders.has(text)) {
          indicesToRemove.push(i);
        }
      });
    } else {
      // Unknown type: remove per-type columns
      ths.forEach((th, i) => {
        const text = (th.textContent || "").trim();
        if (allPerTypeHeaders.includes(text)) {
          indicesToRemove.push(i);
        }
      });
    }

    if (indicesToRemove.length === 0) return html;

    // Remove cells by index in reverse order to preserve positions
    const rows = Array.from(table.querySelectorAll("tr"));
    rows.forEach((tr) => {
      const cells = Array.from(tr.children);
      indicesToRemove
        .slice()
        .sort((a, b) => b - a)
        .forEach((idx) => {
          if (cells[idx]) tr.removeChild(cells[idx]);
        });
    });

    return container.innerHTML;
  } catch (e) {
    // Fail open on any parsing issues
    return html;
  }
};

const getCategories = (func, outputType, graphIndividual, setCategories, setCategory) => {
  const args = {
    function: func,
  };
  args[outputType] = "";
  if (graphIndividual) {
    args["graph-individual"] = "";
  }

  setCategories([]);
  postFetch("get_categories", args)
    .then((response) => {
      const categories = JSON.parse(response);
      setCategories(categories);
      setCategory(categories[0]);
    })
    .catch((err) => console.log(err));
};

export { runAnalysis, makeTableNice, getCategories };
