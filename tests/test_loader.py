from datetime import datetime

def test_table_name(db_table_data):
    assert db_table_data["table_name"] == "news_articles"

def test_columns(db_table_data):
    columns = db_table_data["columns"]
    try:
        assert len(columns) == 5
    except AssertionError:
        print("Wrong columns amount")
    finally:
        assert columns[0] == "title"
        assert columns[1] == "link"
        assert columns[2] == "description"
        assert columns[3] == "pubDate"
        assert columns[4] == "source_id"

def test_rows_data(db_table_data):
    rows = db_table_data["rows"]
    try:
        first_row, second_row, *rest = rows
        if len(rest) > 0:
            print("More than two rows")
            raise AssertionError
    except ValueError:
        print("Less than two")
    else:
        #First row tests
        assert first_row.title == "First Article"
        assert first_row.link == "https://eng-daily.test/article-1"
        assert first_row.description == "Clean description."
        assert first_row.pubDate == "2026-02-18 12:00:00.000000"
        assert first_row.source_id == 1

        #second row tests
        assert second_row.title == "Second Article"
        assert second_row.link == "https://eng-daily.test/article-2"
        assert second_row.description == "Another description."
        assert second_row.pubDate == "2026-02-19 09:30:00.000000"
        assert second_row.source_id == 1