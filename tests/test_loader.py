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
        assert columns[4] == "source"

def test_rows_data(db_table_data):
    rows = db_table_data["rows"]
    try:
        first_row, second_row, *rest = rows
        if len(rest) > 0:
            print("More than two rows")
            raise AssertionError
    except ValueError:
        print("Only one row")
    else:
        
        try:
            assert isinstance(first_row.pubDate, datetime)
            assert isinstance(second_row.pubDate, datetime)
        except AssertionError:
            print(f"Wrong format of pubDate")
        else:
            print(f"Format: {first_row.pubDate}, {second_row.pubDate}")

        #First row tests
        assert first_row.title == "First Article"
        assert first_row.link == "https://eng-daily.test/article-1"
        assert first_row.description == "Clean description."
        assert first_row.source == "Engineering Daily"

        #second row tests
        assert second_row.title == "Second Article"
        assert second_row.link == "https://eng-daily.test/article-2"
        assert second_row.description == "Another description."
        assert second_row.source == "Engineering Daily"