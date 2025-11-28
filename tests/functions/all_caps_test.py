import pytest
from src.functions.definitions.all_caps import (
    AllCaps,
    all_caps_category,
    percent_all_caps_category,
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
                all_caps_category: [2, 1, 0],
                percent_all_caps_category: [66.67, 25.0, 0],
            },
        ),
        (
            "non_group",
            [],
            {
                "Names": ["A", "B"],
                all_caps_category: [2, 1],
                percent_all_caps_category: [50.0, 25.0],
            },
        ),
    ],
    ids=format_param,
)
def test_table(csv, fn_args, expected_result):
    run_table_test(AllCaps(), "all_caps", csv, fn_args, expected_result)


@pytest.mark.parametrize(
    "csv,fn_args,category,graph_individual,expected_result",
    [
        (
            "group",
            [],
            all_caps_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [2, 1]},
            },
        ),
        (
            "group",
            [],
            percent_all_caps_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [40, 33.33]},
            },
        ),
        (
            "group",
            [],
            all_caps_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 1], "B": [1, 0], "C": [0, 0]},
            },
        ),
        (
            "group",
            [],
            percent_all_caps_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [50, 100], "B": [33.33, 0], "C": [0, 0]},
            },
        ),
        (
            "non_group",
            [],
            all_caps_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [2, 1]},
            },
        ),
        (
            "non_group",
            [],
            percent_all_caps_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [40, 33.33]},
            },
        ),
        (
            "non_group",
            [],
            all_caps_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 1], "B": [1, 0]},
            },
        ),
        (
            "non_group",
            [],
            percent_all_caps_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [50, 50], "B": [33.33, 0]},
            },
        ),
    ],
    ids=format_param,
)
def test_graph(csv, fn_args, category, graph_individual, expected_result):
    run_graph_test(
        AllCaps(), "all_caps", csv, fn_args, category, graph_individual, expected_result
    )
