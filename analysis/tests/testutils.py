from datetime import datetime
import pandas as pd
import analysis.utils.constants as constants
from analysis.utils.helpers import is_reaction
from analysis.utils.parse_args import get_analysis_args


def assert_equal(actual, expected, description, test_args):
    try:
        assert actual == expected
    except AssertionError:
        print(
            f"Failed.\n"
            f"Description: {description}\n"
            f"Test args: {test_args}\n"
            f"Actual: {actual}\n"
            f"Expected: {expected}"
        )
        raise (AssertionError)


def assert_table_results_correct(actual, expected):
    for i in range(len(actual)):
        # remove description keys
        description = expected[i]["description"]
        del expected[i]["description"]
        test_args = actual[i]["test args"]
        del actual[i]["test args"]
        assert_equal(actual[i], expected[i], description, test_args)


def assert_graph_results_correct(actual, expected):
    for i in range(len(actual)):
        assert actual[i]["labels"] == expected[i]["labels"]
        for dataset in range(len(actual[i]["datasets"])):
            description = expected[i]["description"]
            test_args = actual[i]["test args"]
            actual_label = actual[i]["datasets"][dataset]["label"]
            expected_label = expected[i]["datasets"][dataset]["label"]
            assert_equal(actual_label, expected_label, description, test_args)
            actual_data = actual[i]["datasets"][dataset]["data"]
            expected_data = expected[i]["datasets"][dataset]["data"]
            assert_equal(actual_data, expected_data, description, test_args)


def get_chat_members(df):
    return df["sender"].unique()


def load_csv(function, csv_name):
    df = pd.read_csv(f"analysis/tests/sample_data/{function}/{csv_name}.csv")
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


def parse_fn_args(function, output_type, *fn_args):
    return get_analysis_args(
        ["--function", function, f"--{output_type}"] + list(fn_args)
    )


def build_printable_test_args(
    fn_name, csv, fn_args, output_type, category=None, indvidual=False
):
    ret = {"function": fn_name, "csv": csv, "fn args": fn_args, "output": output_type}
    if output_type == "graph":
        ret["category"] = category
        ret["graph individual"] = indvidual
    return ret


def generate_table_test_result(
    fn_class,
    fn_name,
    csvs,
    fn_args_combos,
):
    results = []
    for csv in csvs:
        df = load_csv(fn_name, csv)
        for fn_args in fn_args_combos:
            test_args = (
                df,
                parse_fn_args(fn_name, "table", *fn_args),
                get_chat_members(df),
            )
            result = fn_class.run(*test_args)
            result["test args"] = build_printable_test_args(
                fn_name, csv, fn_args, "table"
            )
            results.append(result)
    return results


def generate_graph_test_result(
    fn_class,
    fn_name,
    csvs,
    graph_total_categories,
    graph_individual_categories,
    fn_args_combos,
):
    results = []
    for csv in csvs:
        df = load_csv(fn_name, csv)
        for fn_args in fn_args_combos:
            for category in graph_total_categories:
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
                result["test args"] = build_printable_test_args(
                    fn_name, csv, fn_args, "graph", category, indvidual=False
                )
                results.append(result)
            for category in graph_individual_categories:
                test_args = (
                    df,
                    parse_fn_args(
                        fn_name,
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
                result = fn_class.run(*test_args)
                result["test args"] = build_printable_test_args(
                    fn_name, csv, fn_args, "graph", category, indvidual=True
                )
                results.append(result)
    return results


'''
not used, should delete when i'm confident it will never be used

def generate_sample_messages(
    all_caps_messages=0,
    days=1,
    messages_per_series=1,
    chat_members=3,
):
    """
    Days are used to separate conversations. Each messsage in a day is 1 second after the last (max 1440 messages per day). All days have the same messages.
    """
    start_time="01/01/2000 12:00:00"
    chat_member_names = [chr(member_idx + 65) for member_idx in range(chat_members)]
    while days > 0:
        for member_idx in range(chat_members):
            pass



def generate_sample_message(
    word_count=5,
    word_length=5,
    all_caps=False,
    link=False,
    tweet=False,
    include_emoji=False,
    game_start=False,
    game=False,
    image=False,
    reaction_for=None,
    reaction_type=None,
):
    pass
'''
