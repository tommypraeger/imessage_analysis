import pytest
from analysis.functions.total import (
    Total,
    total_messages_category,
    percent_total_messages_category,
)
from analysis.tests.testutils import *


@pytest.mark.parametrize(
    "csv,fn_args,expected_result",
    [
        (
            "group",
            [],
            {
                "names": ["A", "B", "C"],
                total_messages_category: [6, 3, 3],
                percent_total_messages_category: [50, 25, 25],
            },
        ),
        (
            "non_group",
            [],
            {
                "names": ["A", "B"],
                total_messages_category: [5, 5],
                percent_total_messages_category: [50, 50],
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
                "datasets": {"Total": [4, 8]},
            },
        ),
        (
            "group",
            [],
            total_messages_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [2, 4], "B": [1, 2], "C": [1, 2]},
            },
        ),
        (
            "group",
            [],
            percent_total_messages_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [50, 50], "B": [25, 25], "C": [25, 25]},
            },
        ),
        (
            "non_group",
            [],
            total_messages_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [5, 5]},
            },
        ),
        (
            "non_group",
            [],
            total_messages_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [3, 2], "B": [2, 3]},
            },
        ),
        (
            "non_group",
            [],
            percent_total_messages_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [60, 40], "B": [40, 60]},
            },
        ),
    ],
    ids=format_param,
)
def test_graph(csv, fn_args, category, graph_individual, expected_result):
    run_graph_test(
        Total(), "total", csv, fn_args, category, graph_individual, expected_result
    )
