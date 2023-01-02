from analysis.functions.link import Link, links_category, percent_links_category
from analysis.tests.testutils import *


def test_link():
    fn = Link()
    table_actual = [
        result
        for result in generate_table_test_result(
            fn, "link", csvs=["group", "non_group"], fn_args_combos=[[]]
        )
    ]
    graph_actual = [
        result
        for result in generate_graph_test_result(
            fn,
            "link",
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
            links_category: [1, 1, 0],
            percent_links_category: [50.0, 50.0, 0],
        },
        {
            "description": "non-group",
            "names": ["A", "B"],
            links_category: [1, 1],
            percent_links_category: [25.0, 50.0],
        },
    ]
    graph_expected = [
        {
            "description": "group, total, total messages",
            "datasets": [
                {
                    "label": "Total",
                    "data": [1, 1],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, total, percent messages",
            "datasets": [
                {
                    "label": "Total",
                    "data": [33.33, 33.33],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, total messsages",
            "datasets": [
                {
                    "label": "A",
                    "data": [1, 0],
                },
                {
                    "label": "B",
                    "data": [0, 1],
                },
                {
                    "label": "C",
                    "data": [0, 0],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, percent messsages",
            "datasets": [
                {
                    "label": "A",
                    "data": [100.0, 0],
                },
                {
                    "label": "B",
                    "data": [0, 100.0],
                },
                {
                    "label": "C",
                    "data": [0, 0],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, total messages",
            "datasets": [
                {
                    "label": "Total",
                    "data": [1, 1],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, percent messages",
            "datasets": [
                {
                    "label": "Total",
                    "data": [33.33, 33.33],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, total messsages",
            "datasets": [
                {
                    "label": "A",
                    "data": [1, 0],
                },
                {
                    "label": "B",
                    "data": [0, 1],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, percent messsages",
            "datasets": [
                {
                    "label": "A",
                    "data": [50.0, 0],
                },
                {
                    "label": "B",
                    "data": [0, 100.0],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
    ]
    assert_table_results_correct(table_actual, table_expected)
    assert_graph_results_correct(graph_actual, graph_expected)
