import pytest
from src.functions.definitions.participation import (
    Participation,
    conversations_participated_in_category,
    participation_rate_category,
    participation_rate_no_reactions_category,
    conversations_participated_in_no_reactions_category,
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
            conversations_participated_in_category: [2, 4, 3],
            conversations_participated_in_no_reactions_category: [1, 4, 3],
            participation_rate_category: [50, 100, 75],
            participation_rate_no_reactions_category: [25.0, 100, 75],
        },
    ),
    (
        "group",
        ["--minutes-threshold", "240"],
        {
            "Names": ["A", "B", "C"],
            conversations_participated_in_category: [1, 3, 3],
            conversations_participated_in_no_reactions_category: [1, 3, 3],
            participation_rate_category: [33.33, 100, 100],
            participation_rate_no_reactions_category: [33.33, 100, 100],
        },
    ),
    (
        "non_group",
        [],  # use default
        {
            "Names": ["A", "B"],
            conversations_participated_in_category: [3, 3],
            conversations_participated_in_no_reactions_category: [2, 3],
            participation_rate_category: [75, 75],
            participation_rate_no_reactions_category: [50, 75],
        },
    ),
    (
        "non_group",
        ["--minutes-threshold", "240"],
        {
            "Names": ["A", "B"],
            conversations_participated_in_category: [2, 2],
            conversations_participated_in_no_reactions_category: [2, 2],
            participation_rate_category: [66.67, 66.67],
            participation_rate_no_reactions_category: [66.67, 66.67],
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
                "datasets": {"Total": [2, 3]},
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
                "datasets": {"A": [50.0, 33.33], "B": [100.0, 66.67], "C": [50.0, 66.67]},
            },
        ),
        (
            "group",
            ["--minutes-threshold", "240"],
            conversations_participated_in_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [1, 3]},
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
                "datasets": {"A": [100, 33.33], "B": [100, 66.67], "C": [100, 66.67]},
            },
        ),
        (
            "non_group",
            [],  # use default
            conversations_participated_in_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [2, 3]},
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
                "datasets": {"A": [50, 66.67], "B": [100, 33.33]},
            },
        ),
        (
            "non_group",
            ["--minutes-threshold", "240"],
            conversations_participated_in_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [1, 3]},
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
                "datasets": {"A": [100, 66.67], "B": [100, 33.33]},
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
