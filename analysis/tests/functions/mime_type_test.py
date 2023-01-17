from analysis.functions.mime_type import (
    MimeType,
    type_category,
    percent_type_category,
)
from analysis.tests.testutils import *


def test_mime_type():
    fn = MimeType()
    table_actual = [
        result
        for result in generate_table_test_result(
            fn,
            "mime_type",
            csvs=["group", "non_group"],
            fn_args_combos=[
                ["--mime-type", "text/plain"],
                ["--mime-type", "image/heic"],
            ],
        )
    ]
    graph_actual = [
        result
        for result in generate_graph_test_result(
            fn,
            "mime_type",
            csvs=["group", "non_group"],
            graph_total_categories=fn.get_categories_allowing_graph_total(),
            graph_individual_categories=fn.get_categories(),
            fn_args_combos=[
                ["--mime-type", "text/plain"],
                ["--mime-type", "image/heic"],
            ],
        )
    ]
    table_expected = [
        {
            "description": "group, text/plain",
            "names": ["A", "B", "C"],
            type_category: [3, 1, 2],
            percent_type_category: [50, 25, 33.33],
        },
        {
            "description": "group, image/heic",
            "names": ["A", "B", "C"],
            type_category: [1, 0, 0],
            percent_type_category: [16.67, 0, 0],
        },
        {
            "description": "non-group, text/plain",
            "names": ["A", "B"],
            type_category: [3, 4],
            percent_type_category: [33.33, 50],
        },
        {
            "description": "non-group, image/heic",
            "names": ["A", "B"],
            type_category: [1, 0],
            percent_type_category: [11.11, 0],
        },
    ]
    graph_expected = [
        {
            "description": "group, total, total messages, text/plain",
            "datasets": [
                {
                    "label": "Total",
                    "data": [2, 4],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, total, percent messages, text/plain",
            "datasets": [
                {
                    "label": "Total",
                    "data": [33.33, 40],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, total messsages, text/plain",
            "datasets": [
                {
                    "label": "A",
                    "data": [0, 3],
                },
                {
                    "label": "B",
                    "data": [0, 1],
                },
                {
                    "label": "C",
                    "data": [2, 0],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, percent messsages, text/plain",
            "datasets": [
                {
                    "label": "A",
                    "data": [0, 75],
                },
                {
                    "label": "B",
                    "data": [0, 33.33],
                },
                {
                    "label": "C",
                    "data": [66.67, 0],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, total, total messages, image/heic",
            "datasets": [
                {
                    "label": "Total",
                    "data": [0, 1],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, total, percent messages, image/heic",
            "datasets": [
                {
                    "label": "Total",
                    "data": [0, 10],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, total messsages, image/heic",
            "datasets": [
                {
                    "label": "A",
                    "data": [0, 1],
                },
                {
                    "label": "B",
                    "data": [0, 0],
                },
                {
                    "label": "C",
                    "data": [0, 0],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, percent messsages, image/heic",
            "datasets": [
                {
                    "label": "A",
                    "data": [0, 25],
                },
                {
                    "label": "B",
                    "data": [0, 0],
                },
                {
                    "label": "C",
                    "data": [0, 0],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, total messages, text/plain",
            "datasets": [
                {
                    "label": "Total",
                    "data": [2, 5],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, percent messages, text/plain",
            "datasets": [
                {
                    "label": "Total",
                    "data": [33.33, 45.45],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, total messsages, text/plain",
            "datasets": [
                {
                    "label": "A",
                    "data": [0, 3],
                },
                {
                    "label": "B",
                    "data": [2, 2],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, percent messsages, text/plain",
            "datasets": [
                {
                    "label": "A",
                    "data": [0, 50],
                },
                {
                    "label": "B",
                    "data": [66.67, 40],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, total messages, image/heic",
            "datasets": [
                {
                    "label": "Total",
                    "data": [0, 1],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, percent messages, image/heic",
            "datasets": [
                {
                    "label": "Total",
                    "data": [0, 9.09],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, total messsages, image/heic",
            "datasets": [
                {
                    "label": "A",
                    "data": [0, 1],
                },
                {
                    "label": "B",
                    "data": [0, 0],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, percent messsages, image/heic",
            "datasets": [
                {
                    "label": "A",
                    "data": [0, 16.67],
                },
                {
                    "label": "B",
                    "data": [0, 0],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
    ]
    assert_table_results_correct(table_actual, table_expected)
    assert_graph_results_correct(graph_actual, graph_expected)
