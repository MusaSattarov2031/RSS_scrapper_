import pytest
from sqlalchemy import text, inspect, create_engine
import sqlalchemy as sa
from dotenv import load_dotenv
from os import getenv
from src.loader import load_to_sqlite, execute_query
from src.transformer import transform_to_dataframe
from src.users import UserAuth
from src.subscriptions import SubscriptionManager

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
    # Create in-memory database
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    
    # Create tables 
    conn.execute(text("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """))
    conn.commit()
    
    
    auth = UserAuth(connection=conn)  
    
    auth.create_user("Alex", "password1", "exampleemail@test.com")
    
    yield auth
    
    auth.close()
    conn.close()
    engine.dispose()

@pytest.fixture(scope="session")
def connection(db_url):
    engine = create_engine(db_url)
    conn = engine.connect()
    with engine.connect() as conn:
        yield conn
        print("Closing Connection...")
    print("Connection closed")

@pytest.fixture(scope="session")
def manager():
    sm = SubscriptionManager(db_url="sqlite:///:memory:")
    sm.conn.execute(
        text("""
             CREATE TABLE users(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT,
             password_hash TEXT,
             email TEXT
             )
            """)
    )

    sm.conn.execute(
        text("""
             CREATE TABLE sources(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             source TEXT,
             link TEXT
             )
             """)
    )

    sm.conn.execute(
        text("""
             CREATE TABLE user_subscriptions(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             user_id INTEGER,
             source_id INTEGER,
             FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
             FOREIGN KEY (source_id) REFERENCES sources(id) ON DELETE CASCADE,
             UNIQUE(user_id, source_id)
             )
             """)
    )
    #Insert users
    users = [
        (1, "alice", "hash1", "alice@test.com"),
        (2, "bob", "hash2", "bob@test.com"),
        (3, "charlie", "hash3", "charlie@test.com"),
    ]
    
    for user in users:
        sm.conn.execute(
            text("INSERT INTO users (id, username, password_hash, email) VALUES (:id, :username, :hash, :email)"),
            {"id": user[0], "username": user[1], "hash": user[2], "email": user[3]}
        )
    
    # Insert sources
    sources = [
        (1, "BBC News", "http://feeds.bbci.co.uk/news/rss.xml"),
        (2, "CNN", "http://rss.cnn.com/rss/edition.rss"),
        (3, "TechCrunch", "https://techcrunch.com/feed/"),
        (4, "The Verge", "https://www.theverge.com/rss/index.xml"),
        (5, "NASA", "https://www.nasa.gov/rss/dyn/breaking_news.rss"),
    ]
    
    for source in sources:
        sm.conn.execute(
            text("INSERT INTO sources (id, source, link) VALUES (:id, :source, :link)"),
            {"id": source[0], "source": source[1], "link": source[2]}
        )

    yield sm
    sm.close()