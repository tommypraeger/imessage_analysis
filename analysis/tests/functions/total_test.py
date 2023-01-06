from analysis.functions.total import (
    Total,
    total_messages_category,
    percent_total_messages_category,
)
from analysis.tests.testutils import *


def test_total():
    fn = Total()
    table_actual = [
        result
        for result in generate_table_test_result(
            fn, "total", csvs=["group", "non_group"], fn_args_combos=[[]]
        )
    ]
    graph_actual = [
        result
        for result in generate_graph_test_result(
            fn,
            "total",
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
            total_messages_category: [6, 3, 3],
            percent_total_messages_category: [50, 25, 25],
        },
        {
            "description": "non-group",
            "names": ["A", "B"],
            total_messages_category: [5, 5],
            percent_total_messages_category: [50, 50],
        },
    ]
    graph_expected = [
        {
            "description": "group, total, total messages",
            "datasets": [
                {
                    "label": "Total",
                    "data": [4, 8],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, total messsages",
            "datasets": [
                {
                    "label": "A",
                    "data": [2, 4],
                },
                {
                    "label": "B",
                    "data": [1, 2],
                },
                {
                    "label": "C",
                    "data": [1, 2],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, percent messsages",
            "datasets": [
                {
                    "label": "A",
                    "data": [50, 50],
                },
                {
                    "label": "B",
                    "data": [25, 25],
                },
                {
                    "label": "C",
                    "data": [25, 25],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, total messages",
            "datasets": [
                {
                    "label": "Total",
                    "data": [5, 5],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, total messsages",
            "datasets": [
                {
                    "label": "A",
                    "data": [3, 2],
                },
                {
                    "label": "B",
                    "data": [2, 3],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, percent messsages",
            "datasets": [
                {
                    "label": "A",
                    "data": [60, 40],
                },
                {
                    "label": "B",
                    "data": [40, 60],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
    ]
    assert_table_results_correct(table_actual, table_expected)
    assert_graph_results_correct(graph_actual, graph_expected)
