import pandas as pd

def transform_to_dataframe(parsed_data):
    """Transfrom items of new's data to dataframe with columns:
        title,
        link(unique for each row),
        pubDate in pd.datetime format,
        decription
    """
    try:
        df = pd.DataFrame(parsed_data["items"])
        source = parsed_data["title"]
        arr = [f"{source}" for i in range(df.shape[0])]
        df["source"] = pd.Series(arr)
        df["pubDate"] = pd.to_datetime(df["pubDate"])
        df.drop_duplicates(subset=["link"], inplace=True)
        return df
    except KeyError:
        print("Wrong input format")
