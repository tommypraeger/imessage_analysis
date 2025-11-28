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
                "Names": ["Alice", "Bob", "Carol"],
                CVA_PLUS_CATEGORY: [142.98, 95.68, 61.34],
                VOLUME_COMPONENT_CATEGORY: [105.09, 112.23, 82.68],
                EFFICIENCY_COMPONENT_CATEGORY: [180.87, 79.13, 40.0],
            },
        ),
    ],
    ids=format_param,
)
def test_table(csv, fn_args, expected_result):
    run_table_test(CVAPlus(), "cva_plus", csv, fn_args, expected_result)
