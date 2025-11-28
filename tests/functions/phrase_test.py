import pytest
from src.functions.definitions.phrase import (
    Phrase,
    phrase_category,
    percent_phrase_category,
)
from tests.testutils import *


@pytest.mark.parametrize(
    "csv,fn_args,expected_result",
    [
        (
            "group",
            ["--phrase", "aa"],
            {
                "Names": ["A", "B", "C"],
                phrase_category: [2, 3, 1],
                percent_phrase_category: [100, 100, 50],
            },
        ),
        (
            "group",
            ["--phrase", "aa aa"],
            {
                "Names": ["A", "B", "C"],
                phrase_category: [0, 2, 1],
                percent_phrase_category: [0, 66.67, 50],
            },
        ),
        (
            "group",
            ["--phrase", "AA", "--case-sensitive"],
            {
                "Names": ["A", "B", "C"],
                phrase_category: [0, 1, 1],
                percent_phrase_category: [0, 33.33, 50],
            },
        ),
        (
            "group",
            ["--phrase", "aa", "--separate"],
            {
                "Names": ["A", "B", "C"],
                phrase_category: [1, 2, 1],
                percent_phrase_category: [50, 66.67, 50],
            },
        ),
        (
            "group",
            ["--phrase", "aa aa", "--separate"],
            {
                "Names": ["A", "B", "C"],
                phrase_category: [0, 1, 1],
                percent_phrase_category: [0, 33.33, 50],
            },
        ),
        (
            "group",
            ["--phrase", "aa aa", "--separate", "--case-sensitive"],
            {
                "Names": ["A", "B", "C"],
                phrase_category: [0, 1, 0],
                percent_phrase_category: [0, 33.33, 0],
            },
        ),
        (
            "group",
            ["--phrase", r"[Aa]\s+[Aa]", "--regex"],
            {
                "Names": ["A", "B", "C"],
                phrase_category: [0, 2, 1],
                percent_phrase_category: [0, 66.67, 50],
            },
        ),
        (
            "non_group",
            ["--phrase", "aa"],
            {
                "Names": ["A", "B"],
                phrase_category: [2, 4],
                percent_phrase_category: [100, 80],
            },
        ),
        (
            "non_group",
            ["--phrase", "aa aa"],
            {
                "Names": ["A", "B"],
                phrase_category: [0, 3],
                percent_phrase_category: [0, 60],
            },
        ),
        (
            "non_group",
            ["--phrase", "AA", "--case-sensitive"],
            {
                "Names": ["A", "B"],
                phrase_category: [0, 2],
                percent_phrase_category: [0, 40],
            },
        ),
        (
            "non_group",
            ["--phrase", "aa", "--separate"],
            {
                "Names": ["A", "B"],
                phrase_category: [1, 3],
                percent_phrase_category: [50, 60],
            },
        ),
        (
            "non_group",
            ["--phrase", "aa aa", "--separate"],
            {
                "Names": ["A", "B"],
                phrase_category: [0, 2],
                percent_phrase_category: [0, 40],
            },
        ),
        (
            "non_group",
            ["--phrase", "aa aa", "--separate", "--case-sensitive"],
            {
                "Names": ["A", "B"],
                phrase_category: [0, 1],
                percent_phrase_category: [0, 20],
            },
        ),
        (
            "non_group",
            ["--phrase", r"[Aa]\s+[Aa]", "--regex"],
            {
                "Names": ["A", "B"],
                phrase_category: [0, 3],
                percent_phrase_category: [0, 60],
            },
        ),
    ],
    ids=format_param,
)
def test_table(csv, fn_args, expected_result):
    run_table_test(Phrase(), "phrase", csv, fn_args, apply_phrase_labels(expected_result, fn_args))


@pytest.mark.parametrize(
    "csv,fn_args,category,graph_individual,expected_result",
    [
        (
            "group",
            ["--phrase", "aa"],
            phrase_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [4, 2]},
            },
        ),
        (
            "group",
            ["--phrase", "aa"],
            percent_phrase_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [100, 66.67]},
            },
        ),
        (
            "group",
            ["--phrase", "aa"],
            phrase_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 1], "B": [2, 1], "C": [1, 0]},
            },
        ),
        (
            "group",
            ["--phrase", "aa"],
            percent_phrase_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [100, 100], "B": [100, 100], "C": [100, 0]},
            },
        ),
        (
            "non_group",
            ["--phrase", "aa"],
            phrase_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [4, 2]},
            },
        ),
        (
            "non_group",
            ["--phrase", "aa"],
            percent_phrase_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [100, 66.67]},
            },
        ),
        (
            "non_group",
            ["--phrase", "aa"],
            phrase_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 1], "B": [3, 1]},
            },
        ),
        (
            "non_group",
            ["--phrase", "aa"],
            percent_phrase_category,
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
        Phrase(), "phrase", csv, fn_args, category, graph_individual, expected_result
    )


def apply_phrase_labels(expected_result, fn_args):
    phrase_val = None
    for i, arg in enumerate(fn_args):
        if arg == "--phrase" and i + 1 < len(fn_args):
            phrase_val = fn_args[i + 1]
            break
    if phrase_val is None:
        return expected_result
    phrase_label = phrase_category.replace("the entered phrase", f'"{phrase_val}"')
    percent_label = percent_phrase_category.replace("the entered phrase", f'"{phrase_val}"')
    remapped = {}
    for key, value in expected_result.items():
        if key == phrase_category:
            remapped[phrase_label] = value
        elif key == percent_phrase_category:
            remapped[percent_label] = value
        else:
            remapped[key] = value
    return remapped
