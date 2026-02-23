import pandas as pd
from src.update_sources import insert_source

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
        source_id = insert_source(source, parsed_data["link"])
        # Dataframe creation
        df = pd.DataFrame(parsed_data["items"])
        arr = [source_id for i in range(df.shape[0])]
        df["source_id"] = pd.Series(arr)
        df["pubDate"] = pd.to_datetime(df["pubDate"])
        df.drop_duplicates(subset=["link"], inplace=True)
        return df
    except KeyError:
        print("Wrong input format")