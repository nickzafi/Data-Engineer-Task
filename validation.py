import pandas as pd
from db_connection import *
from models_sql import Netflix

# connect to db
db_engine = initiate_engine(connection_str)

# create connection
connection = db_engine.connect()

# define query fot loading into pandas df
query = "SELECT * FROM netflix"

# read the data into dataframe
df_netflix = pd.read_sql_query(query, connection)
connection.close()


def nan_rows_finder(df):
    """
    Returns a df with nan values
    """
    df_nan_rows = df[df.isna().any(axis=1)]
    return df_nan_rows


def type_validator(df):
    """
    Returns a df with invalid type
    """
    df_invalid_type = df[~(df["type"].isin(["Movie", "TV Show"]))].index
    return df_invalid_type


def date_validator(df):
    """
    Returns a df with invalid date format
    """
    df_invalid_date_format = df[
        ~df.date_added.astype(str).str.contains("\d{4}-\d{2}-\d{2}", regex=True)
    ]
    return df_invalid_date_format


empty_rows = nan_rows_finder(df_netflix).index.values
empty_show_id = nan_rows_finder(df_netflix).show_id.values
show_id_is_unique = df_netflix["show_id"].is_unique
invalid_date_format = date_validator(df_netflix).date_added

# print reporting
print("****REPORT OF MISSING DATA*** ")
print(
    f"The entries corresponding to the following index contain Nan values: {empty_rows}"
)
print("------------------****------------------")
print(f"The show_ids with Nan values are: {empty_show_id}")
print("------------------****------------------")
print("****REPORT OF INVALID / STRANGE DATA*** ")
print("------------------****------------------")
print(f"The show_id column is unique: {show_id_is_unique}")
print("------------------****------------------")
print(f"The wrong formatted dates are: {invalid_date_format}")
