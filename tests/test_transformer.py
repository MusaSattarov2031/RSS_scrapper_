from src.transformer import transform_to_dataframe as tr
import pytest
import pandas as pd

def test_transform(mock_parsed_data):
    df = tr(mock_parsed_data)

    assert isinstance(df, pd.DataFrame)

    assert df.size == 8

    assert df["title"].to_list() == ["First Article", "Second Article"]
