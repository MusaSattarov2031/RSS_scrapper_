from sqlalchemy import engine, text, create_engine
from os import getenv
from dotenv import load_dotenv

def insert_source(source, link):
    load_dotenv()
    db_url = getenv("DATABASE_URL")
    engine = create_engine(db_url)
    conn = engine.connect()
    try:
        source_id = conn.execute(text(f"SELECT id FROM sources WHERE source = '{source}'")).fetchone().id
        print("Such name already presented")
    except AttributeError:
        print("No such a source, creating...")
        result = conn.execute(
            text("""
                INSERT INTO sources (source, link)
                    VALUES (:source, :link)
                """),
                {"source": source, "link": link}
            )
        conn.commit()
        print("Added to table sources")
        source_id = result.lastrowid
    finally:
        engine.dispose()
        print("Returning id")
        return source_id