import pytest
from src.functions.definitions.word_length import (
    WordLength,
    average_word_length_category,
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
                average_word_length_category: [3, 2, 2],
            },
        ),
        (
            "non_group",
            [],
            {
                "Names": ["A", "B"],
                average_word_length_category: [3, 2],
            },
        ),
    ],
    ids=format_param,
)
def test_table(csv, fn_args, expected_result):
    run_table_test(WordLength(), "word_length", csv, fn_args, expected_result)


@pytest.mark.parametrize(
    "csv,fn_args,category,graph_individual,expected_result",
    [
        (
            "group",
            [],
            average_word_length_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [2.11, 2.25]},
            },
        ),
        (
            "group",
            [],
            average_word_length_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [2.5, 4], "B": [2, 2], "C": [0, 2]},
            },
        ),
        (
            "non_group",
            [],
            average_word_length_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [2.11, 2.5]},
            },
        ),
        (
            "non_group",
            [],
            average_word_length_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [2.5, 3.5], "B": [2, 2]},
            },
        ),
    ],
    ids=format_param,
)
def test_graph(csv, fn_args, category, graph_individual, expected_result):
    run_graph_test(
        WordLength(),
        "word_length",
        csv,
        fn_args,
        category,
        graph_individual,
        expected_result,
    )
