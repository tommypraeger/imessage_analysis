from analysis.functions.word_count import WordCount, average_word_count_category
from analysis.tests.testutils import *


def test_word_count():
    fn = WordCount()
    table_actual = [
        result
        for result in generate_table_test_result(
            fn, "word_count", csvs=["group", "non_group"], fn_args_combos=[[]]
        )
    ]
    graph_actual = [
        result
        for result in generate_graph_test_result(
            fn,
            "word_count",
            csvs=["group", "non_group"],
            graph_total_categories=fn.get_categories_allowing_graph_total(),
            graph_individual_categories=fn.get_categories(),
            fn_args_combos=[[]],
        )
    ]
    table_expected = [
        {
            "description": "group",
            "names": ["A", "B", "C"],
            average_word_count_category: [1, 2, 3],
        },
        {
            "description": "non-group",
            "names": ["A", "B"],
            average_word_count_category: [1, 2],
        },
    ]
    graph_expected = [
        {
            "description": "group, total, average",
            "datasets": [
                {
                    "label": "Total",
                    "data": [1.8, 1.75],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, average",
            "datasets": [
                {
                    "label": "A",
                    "data": [1, 1],
                },
                {
                    "label": "B",
                    "data": [2.33, 1.5],
                },
                {
                    "label": "C",
                    "data": [0, 3],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, average",
            "datasets": [
                {
                    "label": "Total",
                    "data": [1.8, 1.25],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, average",
            "datasets": [
                {
                    "label": "A",
                    "data": [1, 1],
                },
                {
                    "label": "B",
                    "data": [2.33, 1.5],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
    ]
    assert_table_results_correct(table_actual, table_expected)
    assert_graph_results_correct(graph_actual, graph_expected)
