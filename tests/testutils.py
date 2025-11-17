from datetime import datetime

import pandas as pd
from src.utils import constants
from src.utils.helpers import is_reaction, parse_date
from src.utils.parse_args import get_analysis_args


def run_table_test(fn_class, fn_name, csv, fn_args, expected_result):
    df = load_csv(fn_name, csv)
    test_args = (
        df,
        parse_fn_args(fn_name, "table", *fn_args),
        get_chat_members(df),
    )
    result, _ = fn_class.run(*test_args)
    assert_equal(result, expected_result)


def run_graph_test(
    fn_class, fn_name, csv, fn_args, category, graph_individual, expected_result
):
    df = load_csv(fn_name, csv)
    if graph_individual:
        fn_args.append("--graph-individual")
    test_args = (
        df,
        parse_fn_args(
            fn_name,
            "graph",
            "--graph-time-interval",
            "day",
            "--category",
            category,
            *fn_args,
        ),
        get_chat_members(df),
    )
    result, _ = fn_class.run(*test_args)
    transform_graph_result(result)
    assert_equal(result, expected_result)


def transform_graph_result(graph_result):
    dataset_dict = {}
    for dataset in graph_result["datasets"]:
        dataset_dict[dataset["label"]] = dataset["data"]
    graph_result["datasets"] = dataset_dict


def assert_equal(actual, expected):
    expected = normalize_expected_labels(expected)
    try:
        assert actual == expected
    except AssertionError:
        print(f"Actual:   {actual}")
        print(f"Expected: {expected}")
        raise AssertionError


def get_chat_members(df):
    return df["sender"].unique()


def load_csv(function, csv_name):
    df = pd.read_csv(
        f"tests/sample_data/{function}/{csv_name}.csv", keep_default_na=False
    )
    if "reaction_to" in df.columns:
        df["reaction_to"] = df["reaction_to"].replace("", pd.NA)
    df["time"] = [parse_date(t) for t in df["time"]]
    if "message_type" not in df.columns:
        mt = pd.Series(["text"] * len(df), dtype="string")
        if "reaction_type" in df.columns:
            raw = df["reaction_type"].astype("string").str.strip()
            mapped = raw.apply(_map_reaction_type_to_message_type)
            mapped = mapped.astype("string")
            mt = mt.mask(mapped.str.len() > 0, mapped)
        if "note" in df.columns:
            note = df["note"].astype("string").str.lower()
            mt = mt.mask(note.str.contains("game start", na=False), "game start")
            mt = mt.mask(note.str.contains("game", na=False), "game")
        df["message_type"] = mt
    return df


def parse_fn_args(function, output_type, *fn_args):
    return get_analysis_args(
        ["--function", function, f"--{output_type}"] + list(fn_args)
    )


def format_param(param):
    if isinstance(param, str):
        return param
    if isinstance(param, list):
        return str(param)
    if isinstance(param, bool):
        if param:
            return "individual"
        return "total"
    if isinstance(param, dict):
        # do not attempt to format expected results
        return ""


def _map_reaction_type_to_message_type(value: str):
    if not value or value.lower() == "nan":
        return ""
    try:
        as_int = int(value)
        return constants.MESSAGE_TYPES.get(as_int, "")
    except ValueError:
        return value


def _normalize_label_value(label):
    if isinstance(label, str):
        for fmt in ("%m/%d/%y", "%m/%d/%Y"):
            try:
                return datetime.strptime(label, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
    return label


def normalize_expected_labels(expected):
    if isinstance(expected, dict):
        normalized = {}
        for key, value in expected.items():
            if key == "labels" and isinstance(value, list):
                normalized[key] = [_normalize_label_value(v) for v in value]
            else:
                normalized[key] = normalize_expected_labels(value)
        return normalized
    if isinstance(expected, list):
        return [normalize_expected_labels(item) for item in expected]
    return expected
