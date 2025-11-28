import pytest
from src.functions.definitions.conversation_starter import (
    ConversationStarter,
    conversations_started_category,
    percent_started_category,
)
from tests.testutils import *


@pytest.mark.parametrize(
    "csv,fn_args,expected_result",
    [
        (
            "group",
            [],  # use default
            {
                "Names": ["A", "B", "C"],
                conversations_started_category: [2, 2, 0],
                percent_started_category: [50, 50, 0],
            },
        ),
        (
            "group",
            ["--minutes-threshold", "240"],
            {
                "Names": ["A", "B", "C"],
                conversations_started_category: [2, 1, 0],
                percent_started_category: [66.67, 33.33, 0],
            },
        ),
        (
            "non_group",
            [],  # use default
            {
                "Names": ["A", "B"],
                conversations_started_category: [2, 2],
                percent_started_category: [50, 50],
            },
        ),
        (
            "non_group",
            ["--minutes-threshold", "240"],
            {
                "Names": ["A", "B"],
                conversations_started_category: [2, 1],
                percent_started_category: [66.67, 33.33],
            },
        ),
    ],
    ids=format_param,
)
def test_table(csv, fn_args, expected_result):
    run_table_test(
        ConversationStarter(), "conversation_starter", csv, fn_args, expected_result
    )


@pytest.mark.parametrize(
    "csv,fn_args,category,graph_individual,expected_result",
    [
        (
            "group",
            [],  # use default
            conversations_started_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [2, 2]},
            },
        ),
        (
            "group",
            [],  # use default
            conversations_started_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 1], "B": [1, 1], "C": [0, 0]},
            },
        ),
        (
            "group",
            [],  # use default
            percent_started_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [50, 50], "B": [50, 50], "C": [0, 0]},
            },
        ),
        (
            "group",
            ["--minutes-threshold", "240"],
            conversations_started_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [1, 2]},
            },
        ),
        (
            "group",
            ["--minutes-threshold", "240"],
            conversations_started_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 1], "B": [0, 1], "C": [0, 0]},
            },
        ),
        (
            "group",
            ["--minutes-threshold", "240"],
            percent_started_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [100, 50], "B": [0, 50], "C": [0, 0]},
            },
        ),
        (
            "non_group",
            [],  # use default
            conversations_started_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [2, 2]},
            },
        ),
        (
            "non_group",
            [],  # use default
            conversations_started_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 1], "B": [1, 1]},
            },
        ),
        (
            "non_group",
            [],  # use default
            percent_started_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [50, 50], "B": [50, 50]},
            },
        ),
        (
            "non_group",
            ["--minutes-threshold", "240"],
            conversations_started_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [1, 2]},
            },
        ),
        (
            "non_group",
            ["--minutes-threshold", "240"],
            conversations_started_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 1], "B": [0, 1]},
            },
        ),
        (
            "non_group",
            ["--minutes-threshold", "240"],
            percent_started_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [100, 50], "B": [0, 50]},
            },
        ),
    ],
    ids=format_param,
)
def test_graph(csv, fn_args, category, graph_individual, expected_result):
    run_graph_test(
        ConversationStarter(),
        "conversation_starter",
        csv,
        fn_args,
        category,
        graph_individual,
        expected_result,
    )
