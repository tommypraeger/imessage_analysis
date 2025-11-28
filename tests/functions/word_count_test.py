import pytest
from src.functions.definitions.word_count import (
    WordCount,
    average_word_count_category,
    total_word_count_category,
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
                average_word_count_category: [1, 2, 3],
                total_word_count_category: [3, 10, 3],
            },
        ),
        (
            "non_group",
            [],
            {
                "Names": ["A", "B"],
                average_word_count_category: [1, 2],
                total_word_count_category: [4, 10],
            },
        ),
    ],
    ids=format_param,
)
def test_table(csv, fn_args, expected_result):
    run_table_test(WordCount(), "word_count", csv, fn_args, expected_result)


@pytest.mark.parametrize(
    "csv,fn_args,category,graph_individual,expected_result",
    [
        (
            "group",
            [],
            average_word_count_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [1.8, 1.75]},
            },
        ),
        (
            "group",
            [],
            average_word_count_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 1], "B": [2.33, 1.5], "C": [0, 3]},
            },
        ),
        (
            "non_group",
            [],
            average_word_count_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [1.8, 1.25]},
            },
        ),
        (
            "non_group",
            [],
            average_word_count_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 1], "B": [2.33, 1.5]},
            },
        ),
    ],
    ids=format_param,
)
def test_graph(csv, fn_args, category, graph_individual, expected_result):
    run_graph_test(
        WordCount(),
        "word_count",
        csv,
        fn_args,
        category,
        graph_individual,
        expected_result,
    )
