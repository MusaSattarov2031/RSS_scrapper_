import pytest
from sqlalchemy import text, inspect, create_engine
import sqlalchemy as sa
from dotenv import load_dotenv
from os import getenv
from src.loader import load_to_sqlite, execute_query
from src.transformer import transform_to_dataframe
from src.users import UserAuth

@pytest.fixture
def google_xml():
    with open("data_samples/google_news.xml", "r") as f:
        return f.read()
    
@pytest.fixture
def empty_xml():
    with open("data_samples/empty_feed.xml", "r") as f:
        return f.read()
    
@pytest.fixture
def error_xml():
    with open("data_samples/invalid/error_page.xml", "r") as f:
        return f.read()
    
@pytest.fixture
def nasa_xml():
    with open("data_samples/nasa_news.xml", "r") as f:
        return f.read()
    
@pytest.fixture
def verge_xml():
    with open("data_samples/the_verge.xml", "r") as f:
        return f.read()

@pytest.fixture
def mock_parsed_data():
    return {
        "title": "Engineering Daily",
        "link": "https://eng-daily.test",
        "items": [
            {
                "title": "First Article",
                "link": "https://eng-daily.test/article-1",
                "description": "Clean description.",
                "pubDate": "Wed, 18 Feb 2026 12:00:00 GMT"
            },
            {
                "title": "First Article (Updated Title)",
                "link": "https://eng-daily.test/article-1",
                "description": "Same link, so this is a duplicate!",
                "pubDate": "Wed, 18 Feb 2026 13:00:00 GMT"
            },
            {
                "title": "Second Article",
                "link": "https://eng-daily.test/article-2",
                "description": "Another description.",
                "pubDate": "Thu, 19 Feb 2026 09:30:00 GMT"
            }
        ]
    }

@pytest.fixture(scope="session")
def db_table_data():
    load_dotenv()
    db_url = getenv("DATABASE_URL")

    engine = create_engine(db_url)

    data = {
        "title": "Engineering Daily",
        "link": "https://eng-daily.test",
        "items": [
            {
                "title": "First Article",
                "link": "https://eng-daily.test/article-1",
                "description": "Clean description.",
                "pubDate": "Wed, 18 Feb 2026 12:00:00 GMT"
            },
            {
                "title": "First Article (Updated Title)",
                "link": "https://eng-daily.test/article-1",
                "description": "Same link, so this is a duplicate!",
                "pubDate": "Wed, 18 Feb 2026 13:00:00 GMT"
            },
            {
                "title": "Second Article",
                "link": "https://eng-daily.test/article-2",
                "description": "Another description.",
                "pubDate": "Thu, 19 Feb 2026 09:30:00 GMT"
            }
        ]
    }

    df = transform_to_dataframe(data)

    load_to_sqlite(df, engine)

    inspector = inspect(engine)
    table_name = inspector.get_table_names()[0]
    rows = execute_query(f"SELECT * FROM {table_name}", engine)

    yield {"table_name": table_name,
            "columns": [col["name"] for col in inspector.get_columns(table_name)],
            "rows": rows}
    
    print("\n Session Teardown: Cleaning up database after all tests")
    with engine.connect() as conn:
        conn.execute(text("Pragma foreign_keys = OFF"))
        
        conn.execute(text(f"DELETE FROM {table_name}"))

        conn.execute(text("Pragma foreign_keys = ON"))
        conn.commit()
    
    engine.dispose()
    print("Session cleanup complete")

@pytest.fixture(scope="session")
def userauth():
    load_dotenv()
    db_url = getenv("DATABASE_URL")

    engine = create_engine(db_url)
    conn = engine.connect()
    auth = UserAuth(conn)
    auth.create_user("Alex", "password1", "exampleemail@test.com")
    yield auth
    print("Clearing Users Table...")
    conn.execute(text("PRAGMA foreign_keys = OFF"))
    conn.execute(text("DELETE FROM users"))
    conn.execute(text("DELETE FROM sqlite_sequence WHERE name = 'users'"))
    conn.execute(text("PRAGMA foreign_keys = ON"))
    conn.commit()
    engine.dispose()
    print("Users table cleared")

@pytest.fixture(scope="session")
def connection():
    load_dotenv()
    db_url = getenv("DATABASE_URL")
    engine = create_engine(db_url)
    with engine.connect() as conn:
        yield conn
        print("Closing Connection...")
    print("Connection closed")