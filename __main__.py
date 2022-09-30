import logging
import sys
from db_connection import initiate_engine
from init_db_schema_from_models import create_schema

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def main():
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

    # create the db
    initiate_engine(connection_str)
    # create schema
    create_schema(connection_str)


if __name__ == "__main__":
    main()
