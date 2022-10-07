from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table, Text
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

Base = declarative_base()
metadata = Base.metadata

# assosiation table
show_genre = Table(
    "show_genre",
    Base.metadata,
    Column("show_id", Integer, ForeignKey("show.id"), primary_key=True, index=True),
    Column(
        "genre_id", Integer, ForeignKey("genre.genre_id"), primary_key=True, index=True
    ),
)

show_country = Table(
    "show_country",
    Base.metadata,
    Column(
        "country_id",
        Integer,
        ForeignKey("countries.country_id"),
        primary_key=True,
        index=True,
    ),
    Column("show_id", Integer, ForeignKey("show.id"), primary_key=True, index=True),
)
show_actor = Table(
    "show_actor",
    Base.metadata,
    Column("show_id", Integer, ForeignKey("show.id"), primary_key=True, index=True),
    Column(
        "actor_id", Integer, ForeignKey("actors.actor_id"), primary_key=True, index=True
    ),
)
show_director = Table(
    "show_director",
    Base.metadata,
    Column("show_id", Integer, ForeignKey("show.id"), primary_key=True, index=True),
    Column(
        "director_id",
        Integer,
        ForeignKey("directors.director_id"),
        primary_key=True,
        index=True,
    ),
)


class Show(Base):
    __tablename__ = "show"
    # __table_args__ = (UniqueConstraint("show_id", "id"), {"schema": "Linkfire"})

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    show_id = Column(VARCHAR(50), index=True, unique=True)
    title = Column(VARCHAR(255), index=True)
    type = Column(VARCHAR(255))
    date_added = Column(DateTime)
    release_year = Column(Integer)
    rating = Column(VARCHAR(50))
    duration = Column(VARCHAR(50))
    description = Column(Text)

    genre_list = relationship("Genre", secondary=show_genre, backref="shows")
    countries_list = relationship(
        "Country", secondary=show_country, backref="countries"
    )
    actors_list = relationship("Actor", secondary=show_actor, backref="actors")
    directors_list = relationship(
        "Director", secondary=show_director, backref="directors"
    )

    def __repr__(self):
        repr_attrs = [
            self.id,
            self.show_id,
            self.type,
            self.title,
            self.date_added,
            self.release_year,
            self.rating,
            self.duration,
            self.description,
        ]
        return f"{self.__class__.__name__} ('{','.join(str(x) for x in repr_attrs)}')"


class Genre(Base):
    __tablename__ = "genre"
    # __table_args__ = {"schema": "Linkfire"}

    genre_id = Column(Integer, primary_key=True)
    genre = Column(VARCHAR(45))

    def __repr__(self):
        repr_attrs = [self.genre_id, self.genre]
        return f"{self.__class__.__name__} ('{','.join(str(x) for x in repr_attrs)}')"


class Country(Base):
    __tablename__ = "countries"

    country_id = Column(Integer, primary_key=True)
    country = Column(VARCHAR(25))

    def __repr__(self):
        repr_attrs = [self.country_id, self.country]
        return f"{self.__class__.__name__} ('{','.join(str(x) for x in repr_attrs)}')"


class Actor(Base):
    __tablename__ = "actors"

    actor_id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR(45))
    last_name = Column(VARCHAR(45))

    def __repr__(self):
        repr_attrs = [self.first_name, self.last_name]
        return f"{self.__class__.__name__} ('{','.join(str(x) for x in repr_attrs)}')"


class Director(Base):
    __tablename__ = "directors"

    director_id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR(45))
    last_name = Column(VARCHAR(45))

    def __repr__(self):
        repr_attrs = [self.first_name, self.last_name]
        return f"{self.__class__.__name__} ('{','.join(str(x) for x in repr_attrs)}')"
