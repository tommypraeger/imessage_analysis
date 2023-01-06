from analysis.functions.emoji import Emoji, emoji_category, percent_emoji_category
from analysis.tests.testutils import *


def test_emoji():
    fn = Emoji()
    table_actual = [
        result
        for result in generate_table_test_result(
            fn, "emoji", csvs=["group", "non_group"], fn_args_combos=[[]]
        )
    ]
    graph_actual = [
        result
        for result in generate_graph_test_result(
            fn,
            "emoji",
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
            emoji_category: [1, 2, 0],
            percent_emoji_category: [16.67, 66.67, 0],
        },
        {
            "description": "non-group",
            "names": ["A", "B"],
            emoji_category: [1, 1],
            percent_emoji_category: [25, 20],
        },
    ]
    graph_expected = [
        {
            "description": "group, total, total messages",
            "datasets": [
                {
                    "label": "Total",
                    "data": [2, 1],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, total, percent messages",
            "datasets": [
                {
                    "label": "Total",
                    "data": [50, 12.5],
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
                    "data": [1, 1],
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
                    "data": [50, 0],
                },
                {
                    "label": "B",
                    "data": [100, 50],
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
                    "data": [2, 0],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, percent messages",
            "datasets": [
                {
                    "label": "Total",
                    "data": [50, 0],
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
                    "data": [1, 0],
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
                    "data": [50, 0],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
    ]
    assert_table_results_correct(table_actual, table_expected)
    assert_graph_results_correct(graph_actual, graph_expected)
