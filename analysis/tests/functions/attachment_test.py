import pytest
from analysis.functions.attachment import (
    Attachment,
    attachment_category,
    percent_attachment_category,
)
from analysis.tests.testutils import *


@pytest.mark.parametrize(
    "csv,fn_args,expected_result",
    [
        (
            "group",
            [],
            {
                "names": ["A", "B", "C"],
                attachment_category: [1, 1, 2],
                percent_attachment_category: [16.67, 25, 33.33],
            },
        ),
        (
            "non_group",
            [],
            {
                "names": ["A", "B"],
                attachment_category: [2, 2],
                percent_attachment_category: [22.22, 25],
            },
        ),
    ],
    ids=format_param,
)
def test_table(csv, fn_args, expected_result):
    run_table_test(Attachment(), "attachment", csv, fn_args, expected_result)


@pytest.mark.parametrize(
    "csv,fn_args,category,graph_individual,expected_result",
    [
        (
            "group",
            [],
            attachment_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [1, 3]},
            },
        ),
        (
            "group",
            [],
            percent_attachment_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [16.67, 30]},
            },
        ),
        (
            "group",
            [],
            attachment_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [0, 1], "B": [0, 1], "C": [1, 1]},
            },
        ),
        (
            "group",
            [],
            percent_attachment_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [0, 25], "B": [0, 33.33], "C": [33.33, 33.33]},
            },
        ),
        (
            "non_group",
            [],
            attachment_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [1, 3]},
            },
        ),
        (
            "non_group",
            [],
            percent_attachment_category,
            False,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"Total": [16.67, 27.27]},
            },
        ),
        (
            "non_group",
            [],
            attachment_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [1, 1], "B": [0, 2]},
            },
        ),
        (
            "non_group",
            [],
            percent_attachment_category,
            True,
            {
                "labels": ["1/1/00", "1/2/00"],
                "datasets": {"A": [33.33, 16.67], "B": [0, 40]},
            },
        ),
    ],
    ids=format_param,
)
def test_graph(csv, fn_args, category, graph_individual, expected_result):
    run_graph_test(
        Attachment(),
        "attachment",
        csv,
        fn_args,
        category,
        graph_individual,
        expected_result,
    )
