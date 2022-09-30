import logging
import sys
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

connection_config_dict = {
    "host": "127.0.0.1",
    "user": "root",
    "port": 0,
    "password": "",
    "database": "Linkfire",
}

db_host = connection_config_dict.get("host")
db_user = connection_config_dict.get("user")
db_port = connection_config_dict.get("port")
db_pwd = connection_config_dict.get("password")
db_name = connection_config_dict.get("database")

# specify connection string
connection_str = f"mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}"
logger.info(f"Connection string: {connection_str}")


def initiate_engine(connection_str):
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
    logger.info("Create engine Succesful")
    return engine
