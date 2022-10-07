import json
import logging
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def load_config(path):
    try:
        with open(path) as data_file:
            config = json.load(data_file)
    except Exception as e:
        raise Exception("Failed to load config{}".format(e))
    return config


def initiate_database(connection_str):
    engine = None
    try:
        engine = create_engine(connection_str)
        # check if database name exists, else create it.
        if not database_exists(engine.url):
            logger.info("Database doesn't exist. Trying to initiate database...")
            create_database(engine.url)
            if database_exists(engine.url):
                logger.info("Database created succesfully")
            else:
                logger.info("Database creation failed")
    except Exception as e:
        raise Exception("Failed to create engine for MySql database {}".format(e))


def initiate_engine(connection_str):
    engine = None
    try:
        engine = create_engine(connection_str)
    except Exception as e:
        raise Exception("Failed to create engine for MySql database {}".format(e))
    logger.info("Create engine Succesful")
    return engine


def initiate_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    return session
