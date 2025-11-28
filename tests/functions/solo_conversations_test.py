import pytest

from src.functions.definitions.solo_conversations import (
    SoloConversations,
    SOLO_COUNT_CATEGORY,
    SOLO_PERCENT_CATEGORY,
)
from tests.testutils import format_param, run_table_test


@pytest.mark.parametrize(
    "csv,fn_args,expected_result",
    [
        (
            "basic",
            [],
            {
                "Names": ["Alice", "Bob", "Carol"],
                SOLO_COUNT_CATEGORY: [0, 1, 0],
                SOLO_PERCENT_CATEGORY: [0.0, 100.0, 0.0],
            },
        ),
    ],
    ids=format_param,
)
def test_table(csv, fn_args, expected_result):
    run_table_test(SoloConversations(), "solo_conversations", csv, fn_args, expected_result)
