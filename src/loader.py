import sqlalchemy as sa
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
engine = sa.create_engine(db_url)

def load_to_sqlite(df: pd.DataFrame, engine: sa.Engine):
    conn = engine.connect()
    df.to_sql("news_articles", conn, if_exists="append", index=False)