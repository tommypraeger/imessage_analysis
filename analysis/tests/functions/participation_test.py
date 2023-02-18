import pytest
from analysis.functions.participation import (
    Participation,
    conversations_participated_in_category,
    participation_rate_category,
)
from analysis.tests.testutils import *


@pytest.mark.parametrize(
    "csv,fn_args,expected_result",
    [
        (
            "group",
            [],  # use default
            {
                "names": ["A", "B", "C"],
                conversations_participated_in_category: [2, 4, 3],
                participation_rate_category: [50, 100, 75],
            },
        ),
        (
            "group",
            ["--minutes-threshold", "240"],
            {
                "names": ["A", "B", "C"],
                conversations_participated_in_category: [2, 3, 3],
                participation_rate_category: [66.67, 100, 100],
            },
        ),
        (
            "non_group",
            [],  # use default
            {
                "names": ["A", "B"],
                conversations_participated_in_category: [3, 3],
                participation_rate_category: [75, 75],
            },
        ),
        (
            "non_group",
            ["--minutes-threshold", "240"],
            {
                "names": ["A", "B"],
                conversations_participated_in_category: [3, 2],
                participation_rate_category: [100, 66.67],
            },
        ),
    ],
    ids=format_param,
)
def test_table(csv, fn_args, expected_result):
    run_table_test(Participation(), "participation", csv, fn_args, expected_result)


@pytest.mark.parametrize(
    "csv,fn_args,category,graph_individual,expected_result",
    [
        (
            "group",
            [],  # use default
            conversations_participated_in_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [2, 2]},
            },
        ),
        (
            "group",
            [],  # use default
            conversations_participated_in_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 1], "B": [2, 2], "C": [1, 2]},
            },
        ),
        (
            "group",
            [],  # use default
            participation_rate_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [50, 50], "B": [100, 100], "C": [50, 100]},
            },
        ),
        (
            "group",
            ["--minutes-threshold", "240"],
            conversations_participated_in_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [1, 2]},
            },
        ),
        (
            "group",
            ["--minutes-threshold", "240"],
            conversations_participated_in_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 1], "B": [1, 2], "C": [1, 2]},
            },
        ),
        (
            "group",
            ["--minutes-threshold", "240"],
            participation_rate_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [100, 50], "B": [100, 100], "C": [100, 100]},
            },
        ),
        (
            "non_group",
            [],  # use default
            conversations_participated_in_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [2, 2]},
            },
        ),
        (
            "non_group",
            [],  # use default
            conversations_participated_in_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 2], "B": [2, 1]},
            },
        ),
        (
            "non_group",
            [],  # use default
            participation_rate_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [50, 100], "B": [100, 50]},
            },
        ),
        (
            "non_group",
            ["--minutes-threshold", "240"],
            conversations_participated_in_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [1, 2]},
            },
        ),
        (
            "non_group",
            ["--minutes-threshold", "240"],
            conversations_participated_in_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 2], "B": [1, 1]},
            },
        ),
        (
            "non_group",
            ["--minutes-threshold", "240"],
            participation_rate_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [100, 100], "B": [100, 50]},
            },
        ),
    ],
    ids=format_param,
)
def test_graph(csv, fn_args, category, graph_individual, expected_result):
    run_graph_test(
        Participation(),
        "participation",
        csv,
        fn_args,
        category,
        graph_individual,
        expected_result,
    )
