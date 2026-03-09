import requests as r
from src.sources import get_sources
from dotenv import load_dotenv
from os import getenv
from sqlalchemy import create_engine
from src.scrapper import parse_xml
from src.transformer import transform_to_dataframe
from src.loader import load_to_sqlite
import pandas as pd

if __name__ == "__main__":
    load_dotenv()
    db_url = getenv("DATABASE_URL")
    engine = create_engine(db_url)
    
    with engine.connect() as conn:
        sources = get_sources(engine)

        for row in sources:
            try:
                id = row.id
                print(f"CONNECTING TO {row.source}: {row.link}")
                xml = r.get(row.link).text
                print("Parsing...")
                dict_data = parse_xml(xml)
                print("Parsed, DataFrame transformation...")
                df = transform_to_dataframe(dict_data, id= row.id, engine=engine)

                links_of_source = pd.read_sql(
                    sql="SELECT link FROM news_articles WHERE source_id = :id",
                    con = conn,
                    params = {"id": id}
                )

                df_filtered = df[~df['link'].isin(links_of_source['link'])]
                size = len(df_filtered)
                print(f"Transformed. Loading to database {size} rows...")
                load_to_sqlite(df_filtered, engine)
            except Exception as e:
                print(f"\n!!! Exception occured: {e} !!!\n")
                continue
    print("COMPLETED")