import pytest
from src.functions.definitions.emoji import (
    Emoji,
    emoji_category,
    percent_emoji_category,
)
from tests.testutils import *


@pytest.mark.parametrize(
    "csv,fn_args,expected_result",
    [
        (
            "group",
            [],
            {
                "names": ["A", "B", "C"],
                emoji_category: [1, 2, 0],
                percent_emoji_category: [16.67, 66.67, 0],
            },
        ),
        (
            "non_group",
            [],
            {
                "names": ["A", "B"],
                emoji_category: [1, 1],
                percent_emoji_category: [25, 20],
            },
        ),
    ],
    ids=format_param,
)
def test_table(csv, fn_args, expected_result):
    run_table_test(Emoji(), "emoji", csv, fn_args, expected_result)


@pytest.mark.parametrize(
    "csv,fn_args,category,graph_individual,expected_result",
    [
        (
            "group",
            [],
            emoji_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [2, 1]},
            },
        ),
        (
            "group",
            [],
            percent_emoji_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [50, 12.5]},
            },
        ),
        (
            "group",
            [],
            emoji_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 0], "B": [1, 1], "C": [0, 0]},
            },
        ),
        (
            "group",
            [],
            percent_emoji_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [50, 0], "B": [100, 50], "C": [0, 0]},
            },
        ),
        (
            "non_group",
            [],
            emoji_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [2, 0]},
            },
        ),
        (
            "non_group",
            [],
            percent_emoji_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [50, 0]},
            },
        ),
        (
            "non_group",
            [],
            emoji_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 0], "B": [1, 0]},
            },
        ),
        (
            "non_group",
            [],
            percent_emoji_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [50, 0], "B": [50, 0]},
            },
        ),
    ],
    ids=format_param,
)
def test_graph(csv, fn_args, category, graph_individual, expected_result):
    run_graph_test(
        Emoji(), "emoji", csv, fn_args, category, graph_individual, expected_result
    )
