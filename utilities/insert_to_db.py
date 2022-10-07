import time
from datetime import datetime
import pandas as pd
from utilities.models_sql import *


def date_transform(date):
    date = date.strip(" ")
    if not date:
        return
    return datetime.strptime(date, "%B %d, %Y").date()


def data_clean(data):
    # s1059 cast is same as description
    if "cast" in data.columns:
        mask = data.cast == data.description
        data.loc[mask, "cast"] = ""
    if "director" in data.columns:
        mask = data.director == data.description
        data.loc[mask, "director"] = ""
    return data


def load_records(dataframe, session):
    dataframe = data_clean(dataframe)
    start = time.time()

    # itterate through dataframe rows.
    for tup in dataframe.itertuples():
        # creating Show
        new_show = Show(
            show_id=tup.show_id,
            title=tup.title,
            type=tup.type,
            date_added=date_transform(tup.date_added),
            release_year=tup.release_year,
            rating=tup.rating,
            duration=tup.duration,
            description=tup.description,
        )

        # adding Show entry
        session.add(new_show)

        # fetch existing genres from db.
        existing_genres = session.query(Genre).all()
        genre_names = [i.genre for i in existing_genres]

        # if genre exists at db, get the id and assign it to the show just added. Else create genre entry ,add it , and assign it.
        for genre_instance in tup.listed_in.split(","):
            genre_instance = genre_instance.strip()
            if genre_instance in genre_names:
                new_show.genre_list.append(
                    session.query(Genre).filter_by(genre=genre_instance).first()
                )
            else:
                new_genre = Genre(genre=genre_instance.strip())
                session.add(new_genre)
                new_show.genre_list.append(new_genre)

        # same goes for countries.
        existing_countries = session.query(Country).all()
        countries_names = [i.country for i in existing_countries]

        for country_instance in tup.country.split(","):
            if country_instance in countries_names:
                new_show.countries_list.append(
                    session.query(Country).filter_by(country=country_instance).first()
                )
            else:
                new_country = Country(country=country_instance.strip())
                session.add(new_country)
                new_show.countries_list.append(new_country)

        # add actors and assosiate them with the shows.
        for actor_instance in tup.cast.split(","):
            actor_first_name = " ".join(
                [name for name in actor_instance.strip().split(" ")][:-1]
            )
            actor_last_name = actor_instance.split(" ")[-1]
            new_actor = Actor(
                first_name=actor_first_name,
                last_name=actor_last_name,
            )
            session.add(new_actor)
            new_show.actors_list.append(new_actor)

        # add directors and assosiate them with the shows.
        for directror_instance in tup.director.split(","):
            director_first_name = " ".join(
                [name for name in directror_instance.strip().split(" ")][:-1]
            )
            director_last_name = directror_instance.split(" ")[-1]
            new_director = Director(
                first_name=director_first_name,
                last_name=director_last_name,
            )
            session.add(new_director)
            new_show.directors_list.append(new_director)

        try:
            session.commit()
        except:
            session.rollback()

    session.close()
    end = time.time()
    print(end - start)
