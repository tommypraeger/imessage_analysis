from datetime import datetime
import pandas as pd
import analysis.utils.constants as constants
from analysis.utils.helpers import is_reaction
from analysis.utils.parse_args import get_analysis_args


def load_csv(csv_name):
    df = pd.read_csv(f"analysis/tests/sample_data/{csv_name}.csv")
    df["is reaction?"] = df["text"].apply(is_reaction)
    df["time"] = [
        datetime(
            int(t[constants.YEAR]),
            int(t[constants.MONTH]),
            int(t[constants.DAY]),
            int(t[constants.HOURS]),
            int(t[constants.MINUTES]),
            int(t[constants.SECONDS]),
        )
        for t in df["time"]
    ]
    return df


def parse_fn_args(function, type, *fn_args):
    return get_analysis_args(["--function", function, f"--{type}"] + list(fn_args))


def assert_table_results_correct(actual, expected):
    for i in range(len(actual)):
        assert actual[i] == expected[i]


def assert_graph_results_correct(actual, expected):
    for i in range(len(actual)):
        assert actual[i]["labels"] == expected[i]["labels"]
        for dataset in range(len(actual[i]["datasets"])):
            assert (
                actual[i]["datasets"][dataset]["label"]
                == expected[i]["datasets"][dataset]["label"]
            )
            assert (
                actual[i]["datasets"][dataset]["data"]
                == expected[i]["datasets"][dataset]["data"]
            )


def get_chat_members(df):
    return df["sender"].unique()


def get_df_list(include_type_col=False, include_reactions=False):
    non_group_df = load_csv("non_group_no_type")
    group_df = load_csv("group_no_type")
    return [non_group_df, group_df]


def generate_table_test_args(
    function, fn_args_combos, include_type_col=False, include_reactions=False
):
    test_args = []
    for df in get_df_list():
        for fn_args in fn_args_combos:
            test_args.append(
                (df, parse_fn_args(function, "table", *fn_args), get_chat_members(df))
            )
    return test_args


def generate_graph_test_args(
    function,
    graph_total_categories,
    graph_individual_categories,
    fn_args_combos,
    include_type_col=False,
    include_reactions=False,
):
    test_args = []
    for df in get_df_list():
        for fn_args in fn_args_combos:
            for category in graph_total_categories:
                test_args.append(
                    (
                        df,
                        parse_fn_args(
                            function,
                            "graph",
                            "--graph-time-interval",
                            "day",
                            "--category",
                            category,
                            *fn_args,
                        ),
                        get_chat_members(df),
                    )
                )
            for category in graph_individual_categories:
                test_args.append(
                    (
                        df,
                        parse_fn_args(
                            function,
                            "graph",
                            "--graph-individual",
                            "--graph-time-interval",
                            "day",
                            "--category",
                            category,
                            *fn_args,
                        ),
                        get_chat_members(df),
                    )
                )
    return test_args
