import csv
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from db_connection import *
from models_sql import Netflix


def date_transform(date):
    date = date.strip(" ")
    if not date:
        return
    return datetime.strptime(date, "%B %d, %Y").date()


records = []
movies = {}
keys = [
    "show_id",
    "type",
    "title",
    "director",
    "cast",
    "country",
    "date_added",
    "release_year",
    "rating",
    "duration",
    "listed_in",
    "description",
]
with open("netflix_titles.csv", "r") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    next(reader, None)
    for row in reader:
        for i, j in enumerate(keys):
            movies[j] = row[i]
            if i == 6:
                movies[j] = date_transform(row[i])
            if i == 7:
                movies[j] = int(row[i])
        records.append(Netflix(**movies))

# connect to db
db_engine = initiate_engine(connection_str)

# create session

Session = sessionmaker(bind=db_engine)
session = Session()

session.add_all(records)

session.commit()

session.close()
