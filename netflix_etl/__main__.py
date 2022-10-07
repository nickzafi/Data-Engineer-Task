import argparse
import logging
import sys
from urllib import parse

from utilities.db_connection import (
    initiate_database,
    initiate_engine,
    initiate_session,
    load_config,
)
from utilities.init_db_schema_from_models import create_schema
from utilities.insert_to_db import *
from utilities.validation import *

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def argparse_specs():
    """
    Command-line argument specification
    """

    parser = argparse.ArgumentParser(
        description="ETL the netflix records from csv to database"
    )
    required_args = parser.add_argument_group("required arguments")
    optional_args = parser.add_argument_group("optional arguments")

    required_args.add_argument("-db", "--database_name", type=str, help="Database name")
    required_args.add_argument(
        "-f", "--file", type=str, help="path to netflix csv file"
    )
    required_args.add_argument(
        "-c", "--config", type=str, help="db connection configuration file"
    )
    optional_args.add_argument("-r", "--report", default=False, help="get data report")
    args = parser.parse_args()
    return args


def main():
    args = argparse_specs()
    connection_config_dict = load_config(args.config)

    db_host = connection_config_dict.get("host")
    db_user = connection_config_dict.get("user")
    db_port = connection_config_dict.get("port")
    db_pwd = connection_config_dict.get("password")
    db_name = args.database_name

    # specify connection string
    connection_str = f"mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}"
    logger.info(f"Connection string: {connection_str}")

    # create the db
    initiate_database(connection_str)
    # create schema
    create_schema(connection_str)
    # create session
    engine = initiate_engine(connection_str)
    session = initiate_session(engine)

    # read csv file
    df_data = pd.read_csv(args.file).fillna("")

    # load records to database
    load_records(df_data, session)

    # get reporting
    report = args.report
    if report:
        validation_report(pd.read_csv(args.file))


if __name__ == "__main__":
    main()
