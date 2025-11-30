import pytest
from src.functions.definitions.message_series import (
    MessageSeries,
    message_series_category,
    average_messages_category,
    percent_series_category,
)
from tests.testutils import *


TABLE_CASES = [
    (
        "group",
        [],
        {
            "Names": ["A", "B", "C"],
            message_series_category: [2, 5, 5],
            average_messages_category: [1.5, 1.0, 1.0],
            percent_series_category: [16.67, 41.67, 41.67],
        },
    ),
    (
        "group",
        ["--minutes-threshold", "240"],
        {
            "Names": ["A", "B", "C"],
            message_series_category: [2, 4, 5],
            average_messages_category: [1.5, 1.25, 1.0],
            percent_series_category: [18.18, 36.36, 45.45],
        },
    ),
    (
        "non_group",
        [],
        {
            "Names": ["A", "B"],
            message_series_category: [5, 5],
            average_messages_category: [1.2, 1.4],
            percent_series_category: [50.0, 50.0],
        },
    ),
    (
        "non_group",
        ["--minutes-threshold", "240"],
        {
            "Names": ["A", "B"],
            message_series_category: [5, 4],
            average_messages_category: [1.2, 1.75],
            percent_series_category: [55.56, 44.44],
        },
    ),
]


@pytest.mark.parametrize("csv,fn_args,expected_result", TABLE_CASES, ids=format_param)
def test_table(csv, fn_args, expected_result):
    run_table_test(MessageSeries(), "message_series", csv, fn_args, expected_result)


GRAPH_CASES = [
    (
        "group",
        [],
        message_series_category,
        False,
        {"labels": ["1/1/00", "1/2/00"], "datasets": {"Total": [6, 6]}},
    ),
    (
        "group",
        [],
        average_messages_category,
        False,
        {"labels": ["1/1/00", "1/2/00"], "datasets": {"Total": [1.17, 1.0]}},
    ),
    (
        "group",
        [],
        message_series_category,
        True,
        {
            "labels": ["1/1/00", "1/2/00"],
            "datasets": {"A": [1, 1], "B": [3, 2], "C": [2, 3]},
        },
    ),
    (
        "group",
        [],
        average_messages_category,
        True,
        {
            "labels": ["1/1/00", "1/2/00"],
            "datasets": {"A": [2.0, 1.0], "B": [1.0, 1.0], "C": [1.0, 1.0]},
        },
    ),
    (
        "group",
        [],
        percent_series_category,
        True,
        {
            "labels": ["1/1/00", "1/2/00"],
            "datasets": {"A": [16.67, 16.67], "B": [50.0, 33.33], "C": [33.33, 50.0]},
        },
    ),
    (
        "group",
        ["--minutes-threshold", "240"],
        message_series_category,
        False,
        {"labels": ["1/1/00", "1/2/00"], "datasets": {"Total": [5, 6]}},
    ),
    (
        "group",
        ["--minutes-threshold", "240"],
        average_messages_category,
        False,
        {"labels": ["1/1/00", "1/2/00"], "datasets": {"Total": [1.4, 1.0]}},
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
            "datasets": {"A": [2.0, 1.0], "B": [1.5, 1.0], "C": [1.0, 1.0]},
        },
    ),
    (
        "group",
        ["--minutes-threshold", "240"],
        percent_series_category,
        True,
        {
            "labels": ["1/1/00", "1/2/00"],
            "datasets": {"A": [20.0, 16.67], "B": [40.0, 33.33], "C": [40.0, 50.0]},
        },
    ),
    (
        "non_group",
        [],
        message_series_category,
        False,
        {"labels": ["1/1/00", "1/2/00"], "datasets": {"Total": [5, 5]}},
    ),
    (
        "non_group",
        [],
        average_messages_category,
        False,
        {"labels": ["1/1/00", "1/2/00"], "datasets": {"Total": [1.4, 1.2]}},
    ),
    (
        "non_group",
        [],
        message_series_category,
        True,
        {"labels": ["1/1/00", "1/2/00"], "datasets": {"A": [2, 3], "B": [3, 2]}},
    ),
    (
        "non_group",
        [],
        average_messages_category,
        True,
        {
            "labels": ["1/1/00", "1/2/00"],
            "datasets": {"A": [1.5, 1.0], "B": [1.33, 1.5]},
        },
    ),
    (
        "non_group",
        [],
        percent_series_category,
        True,
        {
            "labels": ["1/1/00", "1/2/00"],
            "datasets": {"A": [40.0, 60.0], "B": [60.0, 40.0]},
        },
    ),
    (
        "non_group",
        ["--minutes-threshold", "240"],
        message_series_category,
        False,
        {"labels": ["1/1/00", "1/2/00"], "datasets": {"Total": [4, 5]}},
    ),
    (
        "non_group",
        ["--minutes-threshold", "240"],
        average_messages_category,
        False,
        {"labels": ["1/1/00", "1/2/00"], "datasets": {"Total": [1.75, 1.2]}},
    ),
    (
        "non_group",
        ["--minutes-threshold", "240"],
        message_series_category,
        True,
        {"labels": ["1/1/00", "1/2/00"], "datasets": {"A": [2, 3], "B": [2, 2]}},
    ),
    (
        "non_group",
        ["--minutes-threshold", "240"],
        average_messages_category,
        True,
        {
            "labels": ["1/1/00", "1/2/00"],
            "datasets": {"A": [1.5, 1.0], "B": [2.0, 1.5]},
        },
    ),
    (
        "non_group",
        ["--minutes-threshold", "240"],
        percent_series_category,
        True,
        {
            "labels": ["1/1/00", "1/2/00"],
            "datasets": {"A": [50.0, 60.0], "B": [50.0, 40.0]},
        },
    ),
]


@pytest.mark.parametrize(
    "csv,fn_args,category,graph_individual,expected_result",
    GRAPH_CASES,
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
