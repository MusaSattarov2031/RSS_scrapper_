from sqlalchemy import engine, text, create_engine
from os import getenv
from dotenv import load_dotenv

def insert_source(source, link, engine: engine):
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
        conn.close()
        print("Returning id")
        return source_id
    
def remove_source(id = None, source = None, link = None, all = False):
    load_dotenv()
    db_url = getenv("DATABASE_URL")
    engine = create_engine(db_url)
    conn = engine.connect()
    if all:
        conn.execute(text("DELETE FROM sources"))
    elif not (id or source or link):
        print("Provide condition")
    elif id:
        conn.execute(text("DELETE FROM sources WHERE id = :id"), {"id": id})
    elif source:
        conn.execute(text("DELETE FROM sources WHERE source = :source"), {"source": source})
    elif link:
        conn.execute(text("DELETE FROM sources WHERE link = :link"), {"link": link})

    conn.commit()
    engine.dispose()
    return


def get_sources(engine: engine):
    conn = engine.connect()
    result = conn.execute(text("SELECT * FROM sources")).fetchall()
    conn.close()
    return result
