from analysis.functions.all_caps import AllCaps
from analysis.tests.testutils import *


def test_all_caps():
    all_caps_fn = AllCaps()
    table_actual = [
        all_caps_fn.run(*test_args)
        for test_args in generate_table_test_args("all_caps", fn_args_combos=[[]])
    ]
    graph_actual = [
        all_caps_fn.run(*test_args)
        for test_args in generate_graph_test_args(
            "all_caps",
            graph_total_categories=all_caps_fn.get_categories_allowing_graph_total(),
            graph_individual_categories=all_caps_fn.get_categories(),
            fn_args_combos=[[]],
        )
    ]
    table_expected = [
        {
            "names": ["A", "B"],
            "Messages in all caps": [2, 1],
            "Percent of messages that are in all caps": [50.0, 25.0],
        },
        {
            "names": ["A", "B", "C"],
            "Messages in all caps": [3, 2, 0],
            "Percent of messages that are in all caps": [37.5, 50.0, 0],
        },
    ]
    graph_expected = [
        {
            "datasets": [
                {
                    "label": "Total",
                    "data": [2, 1],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "datasets": [
                {
                    "label": "Total",
                    "data": [50.0, 25.0],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "datasets": [
                {
                    "label": "A",
                    "data": [1, 1],
                },
                {
                    "label": "B",
                    "data": [1, 0],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "datasets": [
                {
                    "label": "A",
                    "data": [50.0, 50.0],
                },
                {
                    "label": "B",
                    "data": [50.0, 0],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "datasets": [
                {
                    "label": "Total",
                    "data": [4, 1],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "datasets": [
                {
                    "label": "Total",
                    "data": [50.0, 16.67],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "datasets": [
                {
                    "label": "A",
                    "data": [2, 1],
                },
                {
                    "label": "B",
                    "data": [2, 0],
                },
                {
                    "label": "C",
                    "data": [0, 0],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "datasets": [
                {
                    "label": "A",
                    "data": [50.0, 25.0],
                },
                {
                    "label": "B",
                    "data": [50.0, 0],
                },
                {
                    "label": "C",
                    "data": [0, 0],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
    ]
    assert_table_results_correct(table_actual, table_expected)
    assert_graph_results_correct(graph_actual, graph_expected)
