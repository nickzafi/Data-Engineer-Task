from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Text,
)
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Netflix(Base):
    __tablename__ = "netflix"

    show_id = Column(VARCHAR(20), primary_key=True)
    type = Column(Text(20))
    title = Column(Text(50))
    director = Column(Text(50))
    cast = Column(Text)
    country = Column(Text(50))
    date_added = Column(DateTime)
    release_year = Column(Integer)
    rating = Column(Text(50))
    duration = Column(Text(50))
    listed_in = Column(Text(50))
    description = Column(Text)

    def __repr__(self):
        repr_attrs = [
            self.show_id,
            self.type,
            self.title,
            self.director,
            self.cast,
            self.country,
            self.date_added,
            self.release_year,
            self.rating,
            self.duration,
            self.listed_in,
            self.description,
        ]
        return f"{self.__class__.__name__} ('{','.join(str(x) for x in repr_attrs)}')"
