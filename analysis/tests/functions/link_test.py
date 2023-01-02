from analysis.functions.link import Link
from analysis.tests.testutils import *


def test_link():
    link_fn = Link()
    table_actual = [
        link_fn.run(*test_args)
        for test_args in generate_table_test_args("link", fn_args_combos=[[]])
    ]
    graph_actual = [
        link_fn.run(*test_args)
        for test_args in generate_graph_test_args(
            "link",
            graph_total_categories=link_fn.get_categories_allowing_graph_total(),
            graph_individual_categories=link_fn.get_categories(),
            fn_args_combos=[[]],
        )
    ]
    table_expected = [
        {
            "names": ["A", "B"],
            "Messages that are links": [1, 0],
            "Percent of messages that are links": [25.0, 0],
        },
        {
            "names": ["A", "B", "C"],
            "Messages that are links": [0, 0, 1],
            "Percent of messages that are links": [0, 0, 50.0],
        },
    ]
    graph_expected = [
        {
            "datasets": [
                {
                    "label": "Total",
                    "data": [0, 1],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "datasets": [
                {
                    "label": "Total",
                    "data": [0, 25.0],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
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
            "datasets": [
                {
                    "label": "A",
                    "data": [0, 50],
                },
                {
                    "label": "B",
                    "data": [0, 0],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "datasets": [
                {
                    "label": "Total",
                    "data": [0, 1],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "datasets": [
                {
                    "label": "Total",
                    "data": [0, 16.67],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "datasets": [
                {
                    "label": "A",
                    "data": [0, 0],
                },
                {
                    "label": "B",
                    "data": [0, 0],
                },
                {
                    "label": "C",
                    "data": [0, 1],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "datasets": [
                {
                    "label": "A",
                    "data": [0, 0],
                },
                {
                    "label": "B",
                    "data": [0, 0],
                },
                {
                    "label": "C",
                    "data": [0, 50],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
    ]
    assert_table_results_correct(table_actual, table_expected)
    assert_graph_results_correct(graph_actual, graph_expected)
