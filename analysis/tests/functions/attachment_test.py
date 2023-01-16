from analysis.functions.attachment import (
    Attachment,
    attachment_category,
    percent_attachment_category,
)
from analysis.tests.testutils import *


def test_attachment():
    fn = Attachment()
    table_actual = [
        result
        for result in generate_table_test_result(
            fn, "attachment", csvs=["group", "non_group"], fn_args_combos=[[]]
        )
    ]
    graph_actual = [
        result
        for result in generate_graph_test_result(
            fn,
            "attachment",
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
            attachment_category: [1, 1, 2],
            percent_attachment_category: [16.67, 25, 33.33],
        },
        {
            "description": "non-group",
            "names": ["A", "B"],
            attachment_category: [2, 2],
            percent_attachment_category: [22.22, 25],
        },
    ]
    graph_expected = [
        {
            "description": "group, total, total messages",
            "datasets": [
                {
                    "label": "Total",
                    "data": [1, 3],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, total, percent messages",
            "datasets": [
                {
                    "label": "Total",
                    "data": [16.67, 30],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, total messsages",
            "datasets": [
                {
                    "label": "A",
                    "data": [0, 1],
                },
                {
                    "label": "B",
                    "data": [0, 1],
                },
                {
                    "label": "C",
                    "data": [1, 1],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, percent messsages",
            "datasets": [
                {
                    "label": "A",
                    "data": [0, 25],
                },
                {
                    "label": "B",
                    "data": [0, 33.33],
                },
                {
                    "label": "C",
                    "data": [33.33, 33.33],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, total messages",
            "datasets": [
                {
                    "label": "Total",
                    "data": [1, 3],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, percent messages",
            "datasets": [
                {
                    "label": "Total",
                    "data": [16.67, 27.27],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, total messsages",
            "datasets": [
                {
                    "label": "A",
                    "data": [1, 1],
                },
                {
                    "label": "B",
                    "data": [0, 2],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, percent messsages",
            "datasets": [
                {
                    "label": "A",
                    "data": [33.33, 16.67],
                },
                {
                    "label": "B",
                    "data": [0, 40],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
    ]
    assert_table_results_correct(table_actual, table_expected)
    assert_graph_results_correct(graph_actual, graph_expected)
