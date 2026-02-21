from src.transformer import transform_to_dataframe as tr
import pytest
import pandas as pd

def test_transform(mock_parsed_data):
    df = tr(mock_parsed_data)

    assert isinstance(df, pd.DataFrame)

    assert df.size == 10

    assert df["title"].to_list() == ["First Article", "Second Article"]

    expected_columns = ["title", "link", "description", "pubDate", "source"]
    for col in expected_columns:
        assert col in df.columns