from analysis.functions.word_length import WordLength, average_word_length_category
from analysis.tests.testutils import *


def test_word_length():
    fn = WordLength()
    table_actual = [
        result
        for result in generate_table_test_result(
            fn, "word_length", csvs=["group", "non_group"], fn_args_combos=[[]]
        )
    ]
    graph_actual = [
        result
        for result in generate_graph_test_result(
            fn,
            "word_length",
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
            average_word_length_category: [3, 2, 2],
        },
        {
            "description": "non-group",
            "names": ["A", "B"],
            average_word_length_category: [3, 2],
        },
    ]
    graph_expected = [
        {
            "description": "group, total, average",
            "datasets": [
                {
                    "label": "Total",
                    "data": [2.11, 2.25],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, average",
            "datasets": [
                {
                    "label": "A",
                    "data": [2.5, 4],
                },
                {
                    "label": "B",
                    "data": [2, 2],
                },
                {
                    "label": "C",
                    "data": [0, 2],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, average",
            "datasets": [
                {
                    "label": "Total",
                    "data": [2.11, 2.5],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, average",
            "datasets": [
                {
                    "label": "A",
                    "data": [2.5, 3.5],
                },
                {
                    "label": "B",
                    "data": [2, 2],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
    ]
    assert_table_results_correct(table_actual, table_expected)
    assert_graph_results_correct(graph_actual, graph_expected)
