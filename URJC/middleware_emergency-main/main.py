"""
This script serves as the main entry point for fetching sensor data from the DeepInsight API and storing it in the 'emergency' 
database. It is designed to be flexible, allowing for execution in different environments (locally or on a server) and for 
different time ranges.

The script performs several key steps:
1. Loads SQL credentials based on the execution mode (local or server).
2. Retrieves tracking information for devices and the last load timestamps for data from the database.
3. Loads configuration for data fetching, which includes device identifiers and sensor-variable mappings.
4. Constructs a list of sensor-variable combinations for each device and fetches data for each combination from the DeepInsight API.
5. Stores the fetched data in the database, updating the last load timestamp accordingly.

The script supports command-line arguments to specify the execution mode and optional start/end times for data fetching. 
This allows for automated, scheduled executions as well as ad-hoc data retrieval tasks.

Logging is configured to provide detailed information about the execution process, including any errors encountered, 
making it easier to monitor and debug the data retrieval and storage process.

Usage:
    python main.py --server [local|server] [--init YYYY-MM-DD HH:MM:SS] [--end YYYY-MM-DD HH:MM:SS]

Example:
    python main.py --server local --init "2023-01-01 00:00:00" --end "2023-01-02 00:00:00"

Note: This script assumes that the database and required tables are already set up and that the necessary configurations are 
available in the specified files.
"""

import argparse
from itertools import product
import json
import logging
from logging.handlers import RotatingFileHandler

import numpy as np
from deep_insight_utils import fetch_data
from own_utils import execute_concurrently, load_json
import pandas as pd
import datetime

from sql_utils import get_data


def main(server, init, end, database, logger):
    logger.info("--------------------")
    logger.info("Fetching data from DeepInsight API and storing it in a database.")

    # Import sql parameters
    try :
        creds_file = "sql_without_ssh" if server == "server" else "sql_with_ssh"
        creds_sql = load_json("creds", creds_file)
    except Exception as e:
        logger.error(f"Error loading SQL credentials: {e}")
        raise

    # Load tables from database
    if database is None:
        database = 'emergency'

    # location_device_tracking table
    query_location_device_tracking = f"""
    SELECT *
    FROM location_device_tracking
    """
    try:
        location_device_tracking = get_data(
            database=database,
            query=query_location_device_tracking,
            **creds_sql,
        )
    except Exception as e:
        logger.error(f"Error retrieving data from 'location_device_tracking': {e}")
        raise

    # data_last_load table
    query_data_last_load = f"""
    SELECT *
    FROM data_last_load
    """
    try:
        data_last_load = get_data(
            database=database,
            query=query_data_last_load,
            **creds_sql,
        )
    except Exception as e:
        logger.error(f"Error retrieving data from 'data_last_load': {e}")
        raise

    # data to fetch (filter devices and variables)
    try:
        data_to_fetch = load_json("config","data_to_fetch")
    except Exception as e:
        logger.error(f"Error loading data to fetch in config file: {e}")
        raise


    devices_lot_1 = data_to_fetch["prod_lot_1"]["devices"]
    devices_lot_2 = data_to_fetch["prod_lot_2"]["devices"]

    sensors_variables_emergency_1 = data_to_fetch["prod_lot_1"]["data"]
    sensors_variables_emergency_2 = data_to_fetch["prod_lot_2"]["data"]


    sensor_variable_1 = [(sensor, variable) for (sensor, variables) in sensors_variables_emergency_1.items()
                        for variable in variables]

    beacon_sensor_variable_1 = [(beacon,sensor,variable) for beacon in devices_lot_1 for (sensor, variable) in sensor_variable_1]
    
    

    sensor_variable_2 = [(sensor, variable) for (sensor, variables) in sensors_variables_emergency_2.items()
                        for variable in variables]

    beacon_sensor_variable_2 = [(beacon,sensor,variable) for beacon in devices_lot_2 for (sensor, variable) in sensor_variable_2]
    
    beacon_sensor_variable = beacon_sensor_variable_1 + beacon_sensor_variable_2


    args_list = []
    for beacon, sensor, variable in beacon_sensor_variable:
        id_location = location_device_tracking.query("id_device_current == @beacon")['id_location'].values[0]
        id_variable_inside_db = f"{variable}-{sensor}"
        timestamp_last_load = data_last_load.query("id_device == @beacon and id_sensor == @sensor and id_variable == @id_variable_inside_db")['timestamp_last_load'].values[0]
        timestamp_last_load_str = pd.to_datetime(timestamp_last_load).strftime('%Y-%m-%d %H:%M:%S')
        now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        timestamp_last_load_str = init if init else timestamp_last_load_str
        now_str = end if end else now_str

        # Añadir el diccionario de argumentos para esta iteración a la lista
        args_list.append({
            'id_device': beacon,
            'id_sensor': sensor,
            'id_variable': variable,
            'init_str': timestamp_last_load_str,
            'end_str': now_str,
            'database': database,
            'id_location': id_location,
            'path_save': None,
            'conn_args': creds_sql,
            'logger': logger
        })
        
    execute_concurrently(fetch_data, args_list)

if __name__ == "__main__":

    # command-line arguments
    parser = argparse.ArgumentParser(description="Script to fetch data from DeepInsight API and store it in a database.")
    parser.add_argument("--server", choices=["local", "server"], required=True, help="Execute in local or server mode.")
    parser.add_argument("--init", type=str, help="Start date and time for data fetching (format YYYY-MM-DD HH:MM:SS).", default=None)
    parser.add_argument("--end", type=str, help="End date and time for data fetching (format YYYY-MM-DD HH:MM:SS).", default=None)
    parser.add_argument("--database", type=str, help="Database name to use.", default=None)

    args = parser.parse_args()

    # Set up the logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Define the format for log messages
    formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Handler for writing logs to a file, rotating after reaching 10MB
    file_handler = RotatingFileHandler('logs.log', maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)

    # Handler for displaying logs in the console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    main(
        server=args.server, 
        init=args.init, 
        end=args.end, 
        database=args.database, 
        logger=logger
    )
