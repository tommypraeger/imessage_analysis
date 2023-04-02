import pytest
from src.functions.definitions.message_series import (
    MessageSeries,
    message_series_category,
    average_messages_category,
    percent_series_category,
)
from tests.testutils import *


@pytest.mark.parametrize(
    "csv,fn_args,expected_result",
    [
        (
            "group",
            [],  # use default
            {
                "names": ["A", "B", "C"],
                message_series_category: [2, 5, 5],
                average_messages_category: [2, 1, 1],
                percent_series_category: [16.67, 41.67, 41.67],
            },
        ),
        (
            "group",
            ["--minutes-threshold", "240"],
            {
                "names": ["A", "B", "C"],
                message_series_category: [2, 4, 5],
                average_messages_category: [2, 1.25, 1],
                percent_series_category: [18.18, 36.36, 45.45],
            },
        ),
        (
            "non_group",
            [],  # use default
            {
                "names": ["A", "B"],
                message_series_category: [5, 5],
                average_messages_category: [1.4, 1.4],
                percent_series_category: [50, 50],
            },
        ),
        (
            "non_group",
            ["--minutes-threshold", "240"],
            {
                "names": ["A", "B"],
                message_series_category: [5, 4],
                average_messages_category: [1.4, 1.75],
                percent_series_category: [55.56, 44.44],
            },
        ),
    ],
    ids=format_param,
)
def test_table(csv, fn_args, expected_result):
    run_table_test(MessageSeries(), "message_series", csv, fn_args, expected_result)


@pytest.mark.parametrize(
    "csv,fn_args,category,graph_individual,expected_result",
    [
        (
            "group",
            [],  # use default
            message_series_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [6, 6]},
            },
        ),
        (
            "group",
            [],  # use default
            average_messages_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [1.17, 1.17]},
            },
        ),
        (
            "group",
            [],  # use default
            message_series_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 1], "B": [3, 2], "C": [2, 3]},
            },
        ),
        (
            "group",
            [],  # use default
            average_messages_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [2, 2], "B": [1, 1], "C": [1, 1]},
            },
        ),
        (
            "group",
            [],  # use default
            percent_series_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [16.67, 16.67], "B": [50, 33.33], "C": [33.33, 50]},
            },
        ),
        (
            "group",
            ["--minutes-threshold", "240"],
            message_series_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [5, 6]},
            },
        ),
        (
            "group",
            ["--minutes-threshold", "240"],
            average_messages_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [1.4, 1.17]},
            },
        ),
        (
            "group",
            ["--minutes-threshold", "240"],
            message_series_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 1], "B": [2, 2], "C": [2, 3]},
            },
        ),
        (
            "group",
            ["--minutes-threshold", "240"],
            average_messages_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [2, 2], "B": [1.5, 1], "C": [1, 1]},
            },
        ),
        (
            "group",
            ["--minutes-threshold", "240"],
            percent_series_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [20, 16.67], "B": [40, 33.33], "C": [40, 50]},
            },
        ),
        (
            "non_group",
            [],  # use default
            message_series_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [5, 5]},
            },
        ),
        (
            "non_group",
            [],  # use default
            average_messages_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [1.4, 1.4]},
            },
        ),
        (
            "non_group",
            [],  # use default
            message_series_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [2, 3], "B": [3, 2]},
            },
        ),
        (
            "non_group",
            [],  # use default
            average_messages_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1.5, 1.33], "B": [1.33, 1.5]},
            },
        ),
        (
            "non_group",
            [],  # use default
            percent_series_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [40, 60], "B": [60, 40]},
            },
        ),
        (
            "non_group",
            ["--minutes-threshold", "240"],
            message_series_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [4, 5]},
            },
        ),
        (
            "non_group",
            ["--minutes-threshold", "240"],
            average_messages_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [1.75, 1.4]},
            },
        ),
        (
            "non_group",
            ["--minutes-threshold", "240"],
            message_series_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [2, 3], "B": [2, 2]},
            },
        ),
        (
            "non_group",
            ["--minutes-threshold", "240"],
            average_messages_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1.5, 1.33], "B": [2, 1.5]},
            },
        ),
        (
            "non_group",
            ["--minutes-threshold", "240"],
            percent_series_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [50, 60], "B": [50, 40]},
            },
        ),
    ],
    ids=format_param,
)
def test_graph(csv, fn_args, category, graph_individual, expected_result):
    run_graph_test(
        MessageSeries(),
        "message_series",
        csv,
        fn_args,
        category,
        graph_individual,
        expected_result,
    )
