from analysis.functions.game import (
    Game,
    games_category,
    percent_games_category,
)
from analysis.tests.testutils import *


def test_game():
    fn = Game()
    table_actual = [
        result
        for result in generate_table_test_result(
            fn, "game", csvs=["group", "non_group"], fn_args_combos=[[]]
        )
    ]
    graph_actual = [
        result
        for result in generate_graph_test_result(
            fn,
            "game",
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
            games_category: [2, 2, 2],
            percent_games_category: [33.33, 66.67, 66.67],
        },
        {
            "description": "non-group",
            "names": ["A", "B"],
            games_category: [4, 2],
            percent_games_category: [80, 50],
        },
    ]
    graph_expected = [
        {
            "description": "group, total, total messages",
            "datasets": [
                {
                    "label": "Total",
                    "data": [3, 3],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, total, percent messages",
            "datasets": [
                {
                    "label": "Total",
                    "data": [75, 37.5],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, total messsages",
            "datasets": [
                {
                    "label": "A",
                    "data": [2, 0],
                },
                {
                    "label": "B",
                    "data": [1, 1],
                },
                {
                    "label": "C",
                    "data": [0, 2],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "group, individual, percent messsages",
            "datasets": [
                {
                    "label": "A",
                    "data": [100, 0],
                },
                {
                    "label": "B",
                    "data": [100, 50],
                },
                {
                    "label": "C",
                    "data": [0, 100],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, total messages",
            "datasets": [
                {
                    "label": "Total",
                    "data": [3, 3],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, total, percent messages",
            "datasets": [
                {
                    "label": "Total",
                    "data": [75, 60],
                }
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, total messsages",
            "datasets": [
                {
                    "label": "A",
                    "data": [2, 2],
                },
                {
                    "label": "B",
                    "data": [1, 1],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
        {
            "description": "non-group, individual, percent messsages",
            "datasets": [
                {
                    "label": "A",
                    "data": [100, 66.67],
                },
                {
                    "label": "B",
                    "data": [50, 50],
                },
            ],
            "labels": ["1/1/00", "1/2/00"],
        },
    ]
    assert_table_results_correct(table_actual, table_expected)
    assert_graph_results_correct(graph_actual, graph_expected)
