from analysis.functions.phrase import (
    Phrase,
    phrase_category,
    percent_phrase_category,
)
from analysis.tests.testutils import *


def test_phrase():
    fn = Phrase()
    table_actual = [
        result
        for result in generate_table_test_result(
            fn,
            "phrase",
            csvs=["group", "non_group"],
            fn_args_combos=[
                ["--phrase", "aa"],
                ["--phrase", "aa aa"],
                ["--phrase", "AA", "--case-sensitive"],
                ["--phrase", "aa", "--separate"],
                ["--phrase", "aa aa", "--separate"],
                ["--phrase", "aa aa", "--separate", "--case-sensitive"],
                ["--phrase", r"[Aa]\s+[Aa]", "--regex"],
            ],
        )
    ]
    graph_actual = [
        result
        for result in generate_graph_test_result(
            fn,
            "phrase",
            csvs=["group", "non_group"],
            graph_total_categories=fn.get_categories_allowing_graph_total(),
            graph_individual_categories=fn.get_categories(),
            # not testing as much for graph lol
            fn_args_combos=[
                ["--phrase", "aa"],
            ],
        )
    ]
    table_expected = [
        {
            "description": "group, single word phrase",
            "names": ["A", "B", "C"],
            phrase_category: [2, 3, 1],
            percent_phrase_category: [100, 100, 50],
        },
        {
            "description": "group, multi-word phrase",
            "names": ["A", "B", "C"],
            phrase_category: [0, 2, 1],
            percent_phrase_category: [0, 66.67, 50],
        },
        {
            "description": "group, case sensitive",
            "names": ["A", "B", "C"],
            phrase_category: [0, 1, 1],
            percent_phrase_category: [0, 33.33, 50],
        },
        {
            "description": "group, separate words, one word phrase",
            "names": ["A", "B", "C"],
            phrase_category: [1, 2, 1],
            percent_phrase_category: [50, 66.67, 50],
        },
        {
            "description": "group, separate words, multi-word phrase",
            "names": ["A", "B", "C"],
            phrase_category: [0, 1, 1],
            percent_phrase_category: [0, 33.33, 50],
        },
        {
            "description": "group, separate words, multi-word phrase, case sensitive",
            "names": ["A", "B", "C"],
            phrase_category: [0, 1, 0],
            percent_phrase_category: [0, 33.33, 0],
        },
        {
            "description": "group, regex",
            "names": ["A", "B", "C"],
            phrase_category: [0, 2, 1],
            percent_phrase_category: [0, 66.67, 50],
        },
        {
            "description": "non-group, single word phrase",
            "names": ["A", "B"],
            phrase_category: [2, 4],
            percent_phrase_category: [100, 80],
        },
        {
            "description": "non-group, multi-word phrase",
            "names": ["A", "B"],
            phrase_category: [0, 3],
            percent_phrase_category: [0, 60],
        },
        {
            "description": "non-group, case sensitive",
            "names": ["A", "B"],
            phrase_category: [0, 2],
            percent_phrase_category: [0, 40],
        },
        {
            "description": "non-group, separate words, one word phrase",
            "names": ["A", "B"],
            phrase_category: [1, 3],
            percent_phrase_category: [50, 60],
        },
        {
            "description": "non-group, separate words, multi-word phrase",
            "names": ["A", "B"],
            phrase_category: [0, 2],
            percent_phrase_category: [0, 40],
        },
        {
            "description": "non-group, separate words, multi-word phrase, case sensitive",
            "names": ["A", "B"],
            phrase_category: [0, 1],
            percent_phrase_category: [0, 20],
        },
        {
            "description": "non-group, regex",
            "names": ["A", "B"],
            phrase_category: [0, 3],
            percent_phrase_category: [0, 60],
        },
    ]
    graph_expected = [
        {
            "description": "group, total, total messages, single word phrase",
            "datasets": [
                {
                    "label": "Total",
                    "data": [4, 2],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, total, percent messages, single word phrase",
            "datasets": [
                {
                    "label": "Total",
                    "data": [100, 66.67],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, total messsages, single word phrase",
            "datasets": [
                {
                    "label": "A",
                    "data": [1, 1],
                },
                {
                    "label": "B",
                    "data": [2, 1],
                },
                {
                    "label": "C",
                    "data": [1, 0],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, percent messsages, single word phrase",
            "datasets": [
                {
                    "label": "A",
                    "data": [100, 100],
                },
                {
                    "label": "B",
                    "data": [100, 100],
                },
                {
                    "label": "C",
                    "data": [100, 0],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, total messages, single word phrase",
            "datasets": [
                {
                    "label": "Total",
                    "data": [4, 2],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, percent messages, single word phrase",
            "datasets": [
                {
                    "label": "Total",
                    "data": [100, 66.67],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, total messsages, single word phrase",
            "datasets": [
                {
                    "label": "A",
                    "data": [1, 1],
                },
                {
                    "label": "B",
                    "data": [3, 1],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, percent messsages, single word phrase",
            "datasets": [
                {
                    "label": "A",
                    "data": [100, 100],
                },
                {
                    "label": "B",
                    "data": [100, 50],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
    ]
    assert_table_results_correct(table_actual, table_expected)
    assert_graph_results_correct(graph_actual, graph_expected)
