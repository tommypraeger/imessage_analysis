from analysis.functions.message_series import (
    MessageSeries,
    message_series_category,
    average_messages_category,
    percent_series_category,
)
from analysis.tests.testutils import *


def test_message_series():
    fn = MessageSeries()
    table_actual = [
        result
        for result in generate_table_test_result(
            fn,
            "message_series",
            csvs=["group", "non_group"],
            fn_args_combos=[
                [],  # use default
                ["--minutes-threshold", "240"],
            ],
        )
    ]
    graph_actual = [
        result
        for result in generate_graph_test_result(
            fn,
            "message_series",
            csvs=["group", "non_group"],
            graph_total_categories=fn.get_categories_allowing_graph_total(),
            graph_individual_categories=fn.get_categories(),
            fn_args_combos=[
                [],  # use default
                ["--minutes-threshold", "240"],
            ],
        )
    ]
    table_expected = [
        {
            "description": "group, default minutes threshold",
            "names": ["A", "B", "C"],
            message_series_category: [2, 5, 5],
            average_messages_category: [2, 1, 1],
            percent_series_category: [16.67, 41.67, 41.67],
        },
        {
            "description": "group, custom minutes threshold",
            "names": ["A", "B", "C"],
            message_series_category: [2, 4, 5],
            average_messages_category: [2, 1.25, 1],
            percent_series_category: [18.18, 36.36, 45.45],
        },
        {
            "description": "non-group, default minutes threshold",
            "names": ["A", "B"],
            message_series_category: [5, 5],
            average_messages_category: [1.4, 1.4],
            percent_series_category: [50, 50],
        },
        {
            "description": "non-group, custom minutes threshold",
            "names": ["A", "B"],
            message_series_category: [5, 4],
            average_messages_category: [1.4, 1.75],
            percent_series_category: [55.56, 44.44],
        },
    ]
    graph_expected = [
        {
            "description": "group, total, total series, default minutes threshold",
            "datasets": [
                {
                    "label": "Total",
                    "data": [6, 6],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, total, average per series, default minutes threshold",
            "datasets": [
                {
                    "label": "Total",
                    "data": [1.17, 1.17],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, total series, default minutes threshold",
            "datasets": [
                {
                    "label": "A",
                    "data": [1, 1],
                },
                {
                    "label": "B",
                    "data": [3, 2],
                },
                {
                    "label": "C",
                    "data": [2, 3],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, average per series, default minutes threshold",
            "datasets": [
                {
                    "label": "A",
                    "data": [2, 2],
                },
                {
                    "label": "B",
                    "data": [1, 1],
                },
                {
                    "label": "C",
                    "data": [1, 1],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, percent series, default minutes threshold",
            "datasets": [
                {
                    "label": "A",
                    "data": [16.67, 16.67],
                },
                {
                    "label": "B",
                    "data": [50, 33.33],
                },
                {
                    "label": "C",
                    "data": [33.33, 50],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, total, total series, custom minutes threshold",
            "datasets": [
                {
                    "label": "Total",
                    "data": [5, 6],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, total, average per series, custom minutes threshold",
            "datasets": [
                {
                    "label": "Total",
                    "data": [1.4, 1.17],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, total series, custom minutes threshold",
            "datasets": [
                {
                    "label": "A",
                    "data": [1, 1],
                },
                {
                    "label": "B",
                    "data": [2, 2],
                },
                {
                    "label": "C",
                    "data": [2, 3],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, average per series, custom minutes threshold",
            "datasets": [
                {
                    "label": "A",
                    "data": [2, 2],
                },
                {
                    "label": "B",
                    "data": [1.5, 1],
                },
                {
                    "label": "C",
                    "data": [1, 1],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, percent series, custom minutes threshold",
            "datasets": [
                {
                    "label": "A",
                    "data": [20, 16.67],
                },
                {
                    "label": "B",
                    "data": [40, 33.33],
                },
                {
                    "label": "C",
                    "data": [40, 50],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, total series, default minutes threshold",
            "datasets": [
                {
                    "label": "Total",
                    "data": [5, 5],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, average per series, default minutes threshold",
            "datasets": [
                {
                    "label": "Total",
                    "data": [1.4, 1.4],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, total series, default minutes threshold",
            "datasets": [
                {
                    "label": "A",
                    "data": [2, 3],
                },
                {
                    "label": "B",
                    "data": [3, 2],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, average per series, default minutes threshold",
            "datasets": [
                {
                    "label": "A",
                    "data": [1.5, 1.33],
                },
                {
                    "label": "B",
                    "data": [1.33, 1.5],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, percent series, default minutes threshold",
            "datasets": [
                {
                    "label": "A",
                    "data": [40, 60],
                },
                {
                    "label": "B",
                    "data": [60, 40],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, total series, custom minutes threshold",
            "datasets": [
                {
                    "label": "Total",
                    "data": [4, 5],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, average per series, custom minutes threshold",
            "datasets": [
                {
                    "label": "Total",
                    "data": [1.75, 1.4],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, total series, custom minutes threshold",
            "datasets": [
                {
                    "label": "A",
                    "data": [2, 3],
                },
                {
                    "label": "B",
                    "data": [2, 2],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, average per series, custom minutes threshold",
            "datasets": [
                {
                    "label": "A",
                    "data": [1.5, 1.33],
                },
                {
                    "label": "B",
                    "data": [2, 1.5],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, percent series, custom minutes threshold",
            "datasets": [
                {
                    "label": "A",
                    "data": [50, 60],
                },
                {
                    "label": "B",
                    "data": [50, 40],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
    ]
    assert_table_results_correct(table_actual, table_expected)
    assert_graph_results_correct(graph_actual, graph_expected)
