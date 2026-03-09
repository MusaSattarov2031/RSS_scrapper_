import sqlalchemy as sa
import pandas as pd

def load_to_sqlite(df: pd.DataFrame, engine: sa.Engine):
    conn = engine.connect()
    df.to_sql("news_articles", conn, if_exists="append", index=False)

def execute_query(query: str, engine: sa.engine):
    conn = engine.connect()

    result = conn.execute(sa.text(query)).fetchall()
    conn.commit()
    return result