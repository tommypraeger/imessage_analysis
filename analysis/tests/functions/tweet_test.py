import pytest
from analysis.functions.tweet import Tweet, tweets_category, percent_tweets_category
from analysis.tests.testutils import *


@pytest.mark.parametrize(
    "csv,fn_args,expected_result",
    [
        (
            "group",
            [],
            {
                "names": ["A", "B", "C"],
                tweets_category: [1, 1, 0],
                percent_tweets_category: [50.0, 50.0, 0],
            },
        ),
        (
            "non_group",
            [],
            {
                "names": ["A", "B"],
                tweets_category: [1, 1],
                percent_tweets_category: [25.0, 50.0],
            },
        ),
    ],
    ids=format_param,
)
def test_table(csv, fn_args, expected_result):
    run_table_test(Tweet(), "tweet", csv, fn_args, expected_result)


@pytest.mark.parametrize(
    "csv,fn_args,category,graph_individual,expected_result",
    [
        (
            "group",
            [],
            tweets_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [1, 1]},
            },
        ),
        (
            "group",
            [],
            percent_tweets_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [33.33, 33.33]},
            },
        ),
        (
            "group",
            [],
            tweets_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 0], "B": [0, 1], "C": [0, 0]},
            },
        ),
        (
            "group",
            [],
            percent_tweets_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [100, 0], "B": [0, 100], "C": [0, 0]},
            },
        ),
        (
            "non_group",
            [],
            tweets_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [1, 1]},
            },
        ),
        (
            "non_group",
            [],
            percent_tweets_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [33.33, 33.33]},
            },
        ),
        (
            "non_group",
            [],
            tweets_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 0], "B": [0, 1]},
            },
        ),
        (
            "non_group",
            [],
            percent_tweets_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [50, 0], "B": [0, 100]},
            },
        ),
    ],
    ids=format_param,
)
def test_graph(csv, fn_args, category, graph_individual, expected_result):
    run_graph_test(
        Tweet(), "tweet", csv, fn_args, category, graph_individual, expected_result
    )
