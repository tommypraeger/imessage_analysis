import pytest
from src.functions.definitions.total import (
    Total,
    total_messages_category,
    percent_total_messages_category,
)
from tests.testutils import *


@pytest.mark.parametrize(
    "csv,fn_args,expected_result",
    [
        (
            "group",
            [],
            {
                "Names": ["A", "B", "C"],
                total_messages_category: [5, 3, 3],
                percent_total_messages_category: [45.45, 27.27, 27.27],
            },
        ),
        (
            "non_group",
            [],
            {
                "Names": ["A", "B"],
                total_messages_category: [4, 5],
                percent_total_messages_category: [44.44, 55.56],
            },
        ),
    ],
    ids=format_param,
)
def test_table(csv, fn_args, expected_result):
    run_table_test(Total(), "total", csv, fn_args, expected_result)


@pytest.mark.parametrize(
    "csv,fn_args,category,graph_individual,expected_result",
    [
        (
            "group",
            [],
            total_messages_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [4, 7]},
            },
        ),
        (
            "group",
            [],
            total_messages_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [2, 3], "B": [1, 2], "C": [1, 2]},
            },
        ),
        (
            "group",
            [],
            percent_total_messages_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [50.0, 42.86], "B": [25.0, 28.57], "C": [25.0, 28.57]},
            },
        ),
        (
            "non_group",
            [],
            total_messages_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [4, 5]},
            },
        ),
        (
            "non_group",
            [],
            total_messages_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [2, 2], "B": [2, 3]},
            },
        ),
        (
            "non_group",
            [],
            percent_total_messages_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [50.0, 40.0], "B": [50.0, 60.0]},
            },
        ),
    ],
    ids=format_param,
)
def test_graph(csv, fn_args, category, graph_individual, expected_result):
    run_graph_test(
        Total(), "total", csv, fn_args, category, graph_individual, expected_result
    )
