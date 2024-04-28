import pandas as pd
from src.utils.helpers import is_reaction, parse_date
from src.utils.parse_args import get_analysis_args


def run_table_test(fn_class, fn_name, csv, fn_args, expected_result):
    df = load_csv(fn_name, csv)
    test_args = (
        df,
        parse_fn_args(fn_name, "table", *fn_args),
        get_chat_members(df),
    )
    result = fn_class.run(*test_args)
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
    result = fn_class.run(*test_args)
    transform_graph_result(result)
    assert_equal(result, expected_result)


def transform_graph_result(graph_result):
    dataset_dict = {}
    for dataset in graph_result["datasets"]:
        dataset_dict[dataset["label"]] = dataset["data"]
    graph_result["datasets"] = dataset_dict


def assert_equal(actual, expected):
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
    df["time"] = [parse_date(t) for t in df["time"]]
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
