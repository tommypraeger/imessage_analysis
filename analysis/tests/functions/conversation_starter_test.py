from analysis.functions.conversation_starter import (
    ConversationStarter,
    conversations_started_category,
    percent_started_category,
)
from analysis.tests.testutils import *


def test_conversation_starter():
    fn = ConversationStarter()
    table_actual = [
        result
        for result in generate_table_test_result(
            fn,
            "conversation_starter",
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
            "conversation_starter",
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
            conversations_started_category: [2, 2, 0],
            percent_started_category: [50, 50, 0],
        },
        {
            "description": "group, custom minutes threshold",
            "names": ["A", "B", "C"],
            conversations_started_category: [2, 1, 0],
            percent_started_category: [66.67, 33.33, 0],
        },
        {
            "description": "non-group, default minutes threshold",
            "names": ["A", "B"],
            conversations_started_category: [2, 2],
            percent_started_category: [50, 50],
        },
        {
            "description": "non-group, custom minutes threshold",
            "names": ["A", "B"],
            conversations_started_category: [2, 1],
            percent_started_category: [66.67, 33.33],
        },
    ]
    graph_expected = [
        {
            "description": "group, total, total started, default minutes threshold",
            "datasets": [
                {
                    "label": "Total",
                    "data": [2, 2],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, total started, default minutes threshold",
            "datasets": [
                {
                    "label": "A",
                    "data": [1, 1],
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
            "description": "group, individual, percent started, default minutes threshold",
            "datasets": [
                {
                    "label": "A",
                    "data": [50, 50],
                },
                {
                    "label": "B",
                    "data": [50, 50],
                },
                {
                    "label": "C",
                    "data": [0, 0],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, total, total started, custom minutes threshold",
            "datasets": [
                {
                    "label": "Total",
                    "data": [1, 2],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, total started, custom minutes threshold",
            "datasets": [
                {
                    "label": "A",
                    "data": [1, 1],
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
            "description": "group, individual, percent started, custom minutes threshold",
            "datasets": [
                {
                    "label": "A",
                    "data": [100, 50],
                },
                {
                    "label": "B",
                    "data": [0, 50],
                },
                {
                    "label": "C",
                    "data": [0, 0],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, total started, default minutes threshold",
            "datasets": [
                {
                    "label": "Total",
                    "data": [2, 2],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, total started, default minutes threshold",
            "datasets": [
                {
                    "label": "A",
                    "data": [1, 1],
                },
                {
                    "label": "B",
                    "data": [1, 1],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, percent started, default minutes threshold",
            "datasets": [
                {
                    "label": "A",
                    "data": [50, 50],
                },
                {
                    "label": "B",
                    "data": [50, 50],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, total started, custom minutes threshold",
            "datasets": [
                {
                    "label": "Total",
                    "data": [1, 2],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, total started, custom minutes threshold",
            "datasets": [
                {
                    "label": "A",
                    "data": [1, 1],
                },
                {
                    "label": "B",
                    "data": [0, 1],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, percent started, custom minutes threshold",
            "datasets": [
                {
                    "label": "A",
                    "data": [100, 50],
                },
                {
                    "label": "B",
                    "data": [0, 50],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
    ]
    assert_table_results_correct(table_actual, table_expected)
    assert_graph_results_correct(graph_actual, graph_expected)
