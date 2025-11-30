import pytest
from src.functions.definitions.game import (
    Game,
    games_category,
    percent_games_category,
    game_starts_category,
    percent_game_starts_category,
)
from tests.testutils import *


@pytest.mark.parametrize(
    "csv,fn_args,expected_result",
    [
        (
            "group",
            [],
            {
                "Names": ["A", "B", "C"],
                games_category: [2, 2, 2],
                percent_games_category: [33.33, 66.67, 66.67],
                game_starts_category: [0, 0, 0],
                percent_game_starts_category: [0, 0, 0],
            },
        ),
        (
            "non_group",
            [],
            {
                "Names": ["A", "B"],
                games_category: [4, 2],
                percent_games_category: [80, 50],
                game_starts_category: [0, 0],
                percent_game_starts_category: [0, 0],
            },
        ),
    ],
    ids=format_param,
)
def test_table(csv, fn_args, expected_result):
    run_table_test(Game(), "game", csv, fn_args, expected_result)


@pytest.mark.parametrize(
    "csv,fn_args,category,graph_individual,expected_result",
    [
        (
            "group",
            [],
            games_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [3, 3]},
            },
        ),
        (
            "group",
            [],
            percent_games_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [75, 37.5]},
            },
        ),
        (
            "group",
            [],
            games_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [2, 0], "B": [1, 1], "C": [0, 2]},
            },
        ),
        (
            "group",
            [],
            percent_games_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [100, 0], "B": [100, 50], "C": [0, 100]},
            },
        ),
        (
            "non_group",
            [],
            games_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [3, 3]},
            },
        ),
        (
            "non_group",
            [],
            percent_games_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [75, 60]},
            },
        ),
        (
            "non_group",
            [],
            games_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [2, 2], "B": [1, 1]},
            },
        ),
        (
            "non_group",
            [],
            percent_games_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [100, 66.67], "B": [50, 50]},
            },
        ),
    ],
    ids=format_param,
)
def test_graph(csv, fn_args, category, graph_individual, expected_result):
    run_graph_test(
        Game(), "game", csv, fn_args, category, graph_individual, expected_result
    )
