from analysis.functions.total import (
    Total,
    total_messages_category,
    percent_total_messages_category,
)
from analysis.tests.testutils import *


total_test = FunctionTest(Total(), "total")


def test_table__group():
    total_test.run_table_test(
        csv="group",
        fn_args=[],
        expected_result={
            "names": ["A", "B", "C"],
            total_messages_category: [6, 3, 3],
            percent_total_messages_category: [50, 25, 25],
        },
    )


def test_table__non_group():
    total_test.run_table_test(
        csv="non_group",
        fn_args=[],
        expected_result={
            "names": ["A", "B"],
            total_messages_category: [5, 5],
            percent_total_messages_category: [50, 50],
        },
    )


def test_graph__group__total__total_messages():
    total_test.run_graph_test(
        csv="group",
        fn_args=[],
        category=total_messages_category,
        graph_individual=False,
        expected_result={
            "datasets": {"Total": [4, 8]},
            "labels": ["1/1/00", "1/2/00"],
        },
    )


def test_graph__group__individual__total_messages():
    total_test.run_graph_test(
        csv="group",
        fn_args=[],
        category=total_messages_category,
        graph_individual=True,
        expected_result={
            "datasets": {"A": [2, 4], "B": [1, 2], "C": [1, 2]},
            "labels": ["1/1/00", "1/2/00"],
        },
    )


def test_graph__group__individual__percent_messages():
    total_test.run_graph_test(
        csv="group",
        fn_args=[],
        category=percent_total_messages_category,
        graph_individual=True,
        expected_result={
            "datasets": {"A": [50, 50], "B": [25, 25], "C": [25, 25]},
            "labels": ["1/1/00", "1/2/00"],
        },
    )


def test_graph__non_group__total__total_messages():
    total_test.run_graph_test(
        csv="non_group",
        fn_args=[],
        category=total_messages_category,
        graph_individual=False,
        expected_result={
            "datasets": {"Total": [5, 5]},
            "labels": ["1/1/00", "1/2/00"],
        },
    )


def test_graph__non_group__individual__total_messages():
    total_test.run_graph_test(
        csv="non_group",
        fn_args=[],
        category=total_messages_category,
        graph_individual=True,
        expected_result={
            "datasets": {"A": [3, 2], "B": [2, 3]},
            "labels": ["1/1/00", "1/2/00"],
        },
    )


def test_graph__non_group__individual__percent_messages():
    total_test.run_graph_test(
        csv="non_group",
        fn_args=[],
        category=percent_total_messages_category,
        graph_individual=True,
        expected_result={
            "datasets": {"A": [60, 40], "B": [40, 60]},
            "labels": ["1/1/00", "1/2/00"],
        },
    )
