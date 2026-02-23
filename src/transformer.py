import pandas as pd
import sqlalchemy as sa
from os import getenv

def transform_to_dataframe(parsed_data):
    """Transfrom items of new's data to dataframe with columns:
        title,
        link(unique for each row),
        pubDate in pd.datetime format,
        decription,
        source_id
    """
    try:
        #Get source_id from db
        source = parsed_data["title"]
        db_url = getenv("DATABASE_URL")
        engine = sa.create_engine(db_url)
        conn = engine.connect()
        source_id = conn.execute(sa.text(f"SELECT id FROM sources WHERE source = {source}")).fetchone().id
        engine.dispose()


        # Dataframe creation
        df = pd.DataFrame(parsed_data["items"])
        arr = [source_id for i in range(df.shape[0])]
        df["source"] = pd.Series(arr)
        df["pubDate"] = pd.to_datetime(df["pubDate"])
        df.drop_duplicates(subset=["link"], inplace=True)
        return df
    except KeyError:
        print("Wrong input format")
