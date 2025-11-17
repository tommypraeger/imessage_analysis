import pytest

from src.functions.definitions.cva_plus import (
    CVAPlus,
    CVA_PLUS_CATEGORY,
    VOLUME_COMPONENT_CATEGORY,
    EFFICIENCY_COMPONENT_CATEGORY,
)
from tests.testutils import format_param, run_table_test


@pytest.mark.parametrize(
    "csv,fn_args,expected_result",
    [
        (
            "basic",
            [],
            {
                "names": ["Alice", "Bob", "Carol"],
                CVA_PLUS_CATEGORY: [152.43, 76.57, 71.0],
                VOLUME_COMPONENT_CATEGORY: [104.0, 114.0, 82.0],
                EFFICIENCY_COMPONENT_CATEGORY: [200.87, 39.13, 60.0],
            },
        ),
    ],
    ids=format_param,
)
def test_table(csv, fn_args, expected_result):
    run_table_test(CVAPlus(), "cva_plus", csv, fn_args, expected_result)
