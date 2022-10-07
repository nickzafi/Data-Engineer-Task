import logging
import sys

from utilities.db_connection import initiate_engine
from utilities.models_sql import Base

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def create_schema(connection_str: str):
    """
    Create table schema from models_sql.py for given connection str
    """
    try:
        # create engine
        engine = initiate_engine(connection_str)
        # create tables defined at models_sql.py
        Base.metadata.create_all(engine)
        logger.info("Tables created")
    except Exception as e:
        raise Exception("Failed to create schema {}".format(e))
