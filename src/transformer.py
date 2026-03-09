import pandas as pd
from src.sources import insert_source

def transform_to_dataframe(parsed_data, engine,id = None):
    """Transfrom items of new's data to dataframe with columns:
        title,
        link(unique for each row),
        pubDate in pd.datetime format,
        description,
        source_id
    """
    try:
        #Get source_id from db
        if not id:
            source = parsed_data["title"]
            source_id = insert_source(source, parsed_data["link"], engine)
        else:
            source_id = id
        # Dataframe creation
        df = pd.DataFrame(parsed_data["items"])
        df["source_id"] = source_id
        df["pubDate"] = pd.to_datetime(df["pubDate"])
        df.drop_duplicates(subset=["link"], inplace=True)
        return df
    except KeyError:
        print("Wrong input format")