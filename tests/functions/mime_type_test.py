import pytest
from src.functions.definitions.mime_type import (
    MimeType,
    type_category,
    percent_type_category,
)
from tests.testutils import *


@pytest.mark.parametrize(
    "csv,fn_args,expected_result",
    [
        (
            "group",
            ["--mime-type", "text/plain"],
            {
                "names": ["A", "B", "C"],
                type_category: [3, 1, 2],
                percent_type_category: [50, 25, 33.33],
            },
        ),
        (
            "group",
            ["--mime-type", "image/heic"],
            {
                "names": ["A", "B", "C"],
                type_category: [1, 0, 0],
                percent_type_category: [16.67, 0, 0],
            },
        ),
        (
            "non_group",
            ["--mime-type", "text/plain"],
            {
                "names": ["A", "B"],
                type_category: [3, 4],
                percent_type_category: [33.33, 50],
            },
        ),
        (
            "non_group",
            ["--mime-type", "image/heic"],
            {
                "names": ["A", "B"],
                type_category: [1, 0],
                percent_type_category: [11.11, 0],
            },
        ),
    ],
    ids=format_param,
)
def test_table(csv, fn_args, expected_result):
    run_table_test(MimeType(), "mime_type", csv, fn_args, expected_result)


@pytest.mark.parametrize(
    "csv,fn_args,category,graph_individual,expected_result",
    [
        (
            "group",
            ["--mime-type", "text/plain"],
            type_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [2, 4]},
            },
        ),
        (
            "group",
            ["--mime-type", "text/plain"],
            percent_type_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [33.33, 40]},
            },
        ),
        (
            "group",
            ["--mime-type", "text/plain"],
            type_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [0, 3], "B": [0, 1], "C": [2, 0]},
            },
        ),
        (
            "group",
            ["--mime-type", "text/plain"],
            percent_type_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [0, 75], "B": [0, 33.33], "C": [66.67, 0]},
            },
        ),
        (
            "group",
            ["--mime-type", "image/heic"],
            type_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [0, 1]},
            },
        ),
        (
            "group",
            ["--mime-type", "image/heic"],
            percent_type_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [0, 10]},
            },
        ),
        (
            "group",
            ["--mime-type", "image/heic"],
            type_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [0, 1], "B": [0, 0], "C": [0, 0]},
            },
        ),
        (
            "group",
            ["--mime-type", "image/heic"],
            percent_type_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [0, 25], "B": [0, 0], "C": [0, 0]},
            },
        ),
        (
            "non_group",
            ["--mime-type", "text/plain"],
            type_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [2, 5]},
            },
        ),
        (
            "non_group",
            ["--mime-type", "text/plain"],
            percent_type_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [33.33, 45.45]},
            },
        ),
        (
            "non_group",
            ["--mime-type", "text/plain"],
            type_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [0, 3], "B": [2, 2]},
            },
        ),
        (
            "non_group",
            ["--mime-type", "text/plain"],
            percent_type_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [0, 50], "B": [66.67, 40]},
            },
        ),
        (
            "non_group",
            ["--mime-type", "image/heic"],
            type_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [0, 1]},
            },
        ),
        (
            "non_group",
            ["--mime-type", "image/heic"],
            percent_type_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [0, 9.09]},
            },
        ),
        (
            "non_group",
            ["--mime-type", "image/heic"],
            type_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [0, 1], "B": [0, 0]},
            },
        ),
        (
            "non_group",
            ["--mime-type", "image/heic"],
            percent_type_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [0, 16.67], "B": [0, 0]},
            },
        ),
    ],
    ids=format_param,
)
def test_graph(csv, fn_args, category, graph_individual, expected_result):
    run_graph_test(
        MimeType(),
        "mime_type",
        csv,
        fn_args,
        category,
        graph_individual,
        expected_result,
    )
