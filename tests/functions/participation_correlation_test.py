import re

import pandas as pd
import pytest

from src.functions.definitions.participation_correlation import ParticipationCorrelation
from tests.testutils import get_chat_members, get_analysis_args, load_csv


def _parse_html_table(html: str) -> pd.DataFrame:
    rows = re.findall(r"<tr>(.*?)</tr>", html, flags=re.S)
    data = []
    for row in rows:
        cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", row, flags=re.S)
        data.append([re.sub(r"<[^>]+>", "", c).strip() for c in cells])
    header = data[0][1:]
    body = []
    index = []
    for r in data[1:]:
        index.append(r[0])
        body.append([float(val) for val in r[1:]])
    return pd.DataFrame(body, index=index, columns=header)


@pytest.mark.parametrize(
    "csv,expected_matrix",
    [
        (
            "group",
            pd.DataFrame(
                [[1.0, 0.0, 0.33], [0.0, 1.0, 0.0], [0.33, 0.0, 1.0]],
                index=["A", "B", "C"],
                columns=["A", "B", "C"],
            ),
        ),
        (
            "non_group",
            pd.DataFrame(
                [[1.0, -0.58], [-0.58, 1.0]],
                index=["A", "B"],
                columns=["A", "B"],
            ),
        ),
    ],
)
def test_table(csv, expected_matrix):
    df = load_csv("participation", csv)
    args = get_analysis_args(["--function", "participation_correlation", "--table"])
    result, _ = ParticipationCorrelation().run(df, args, get_chat_members(df))
    table_data = result.get("tableData")
    assert table_data is not None
    headers = table_data["headers"]
    rows = table_data["rows"]
    assert headers[0] == ""
    names = headers[1:]
    parsed = pd.DataFrame([r[1:] for r in rows], index=[r[0] for r in rows], columns=names)
    parsed = parsed.loc[expected_matrix.index, expected_matrix.columns]
    assert parsed.round(2).equals(expected_matrix)
