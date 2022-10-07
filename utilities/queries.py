import pandas as pd
from sqlalchemy.orm import sessionmaker
from utilities.db_connection import *
from utilities.models_sql import *

# connect to db
db_engine = initiate_engine(connection_str)

# create connection
connection = db_engine.connect()

# define query for loading into pandas df
query = "SELECT * FROM Linkfire"

# read the data into dataframe
df_netflix = pd.read_sql_query(query, connection)

# create session
Session = sessionmaker(bind=db_engine)
session = Session()
# fetch cast
cast = session.query(Linkfire).with_entities(Linkfire.cast).all()

session.close()
connection.close()

# find actor occurances
actors = []
for row in cast:
    actors.append(row[0].split(","))
actors = [actor for sublist in actors for actor in sublist]
actors_df = pd.DataFrame(actors)
actors_df.columns = ["name"]


# What is the most common first name among actors and actresses?

df_gender = pd.read_csv("gender.csv")
df_gender.columns = ["name", "gender"]
df_gender[["", "first_name", "last_name"]] = df_gender["name"].str.split(
    " ", n=2, expand=True
)
print(df_gender.groupby(["gender", "first_name"]).size().sort_values(ascending=False))

# Which Movie had the longest timespan from release to appearing on Netflix?

# pandas
df_netflix["longest_timespan"] = df_netflix.apply(
    lambda row: int(row.release_year) - row.date_added.year, axis=1
)
print(
    "The show with longest timespan:",
    df_netflix.sort_values(by=["longest_timespan"]).reset_index()["title"][0],
)

# SQL
query = """
        select show_id, title,  date_added, release_year, year(date_added) - release_year year_diff
        from Linkfire.show
        where release_year < year(date_added)
        order by year_diff desc limit 1;
        """
# ANSWER:
# s4868, Pioneers:First Women Filmmakers, year diff 93

# Which Month of the year had the most new releases historically?
query = """
        select count(id) num, month(date_added) mon, year(date_added) yea from Linkfire.show
        group by mon, yea
        order by num desc limit 1;
        """
# ANSWER:
# Nov, 2019  count 272

# Which year had the largest increase year on year (percentage wise) for TV Shows?

# List the actresses that have appeared in a movie with Woody Harrelson more than once.
