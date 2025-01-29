"""
This module provides utilities for interacting with sensor data APIs, processing the fetched data, and interfacing with SQL 
databases. The functions included enable:

1. `get_data_api_time`: Fetches sensor data from an API based on provided time ranges and sensor identifiers. 
It constructs an API request using sensor and beacon IDs, along with a specified channel and time range, 
to retrieve data in JSON format.

2. `fix_units_emergency`: Adjusts the units of sensor data based on the sensor type. This function applies predefined scaling 
factors to raw sensor values to convert them into meaningful units, facilitating data interpretation and analysis.

3. `fetch_data`: Retrieves and processes data for a specific device, sensor, and variable within a given time frame. 
This function encapsulates the process of data fetching, unit adjustment, and optional local/SQL database storage. 
It is designed to handle data retrieval in a robust manner, accounting for potential API limitations or server-side restrictions
 on concurrent connections.

The module is designed to support a flexible data acquisition system, allowing for easy integration with various sensor types and
 data storage solutions. It emphasizes error handling and data integrity, ensuring reliable data retrieval and storage operations.

"""

import datetime
import numpy as np
import pandas as pd

import requests

from sql_utils import update_values, write_data


def get_data_api_time(id_sensor, id_beacon, channelid, init_str, end_str, logger = None):
    """
    Retrieves data from an API based on provided time range and identifiers.
   
    Parameters:
    id_sensor (str): Sensor identifier.
    id_beacon (str): Beacon identifier.
    channelid (str): Channel identifier.
    init_str (str): Initial date-time as string in the format '%Y-%m-%d %H:%M:%S'.
    end_str (str): End date-time as string in the format '%Y-%m-%d %H:%M:%S'.
   
    Returns:
    dict: JSON response from the API. None if an exception occurs or status code is not 200.
   
    Examples:
    >>> get_data_api_time('sAQU', 'DBEM002', '00-eco2', '2023-06-12 00:00:00', '2023-06-14 00:00:00')
    {
        'time': ['2023-06-12 11:07:40.000000', '2023-06-12 11:07:50.000000', ...],
        'value': [400.0, 400.0, ...]
    }
 
    API allowed parameters:
    - id_sensor/channelid: Keys represent id_sensor. Values represent channelid. This works for beacons between 1 and 8:
        DBEM001,DBEM002,DBEM003,DBEM004,DBEM005,DBEM006,DBEM007,DBEM008
        {
            "sSMON":
                [
                    '00-temp',
                    '01-hum',
                    '02-bat',
                    '03-pg'
                ],
            "sWEA":
                [
                    '00-temp',
                    '01-hum',
                    '02-pres',
                    '03-siaq',
                    '04-diaq',
                    'Q0-asiaq',
                    'Q1-adiaq'
                ],
            "sAQU":
                [
                    '00-eco2',
                    '01-tvoc',
                    'Q0-calib'
                ],
            "sACC":
                [
                    '00-accx',
                    '01-accy',
                    '02-accz'
                ]
            ,
            "sALM":
                [
                    '00-almtemp',
                    '01-almbat',
                    '02-almsiaq',
                    '03-almeco2',
                    '04-almtvoc'
                ]
        }
   
    """

    # API format: Concatenating id_sensor and id_beacon to form objectid
    objectid = f"{id_sensor}{id_beacon}-0"
 
    # Defining the input and API time formats
    input_time_format = '%Y-%m-%d %H:%M:%S'
    api_time_format = '%Y-%m-%d %H:%M:%S.%f'
   
    # Converting init_str and end_str to the required API time format
    init = datetime.datetime.strptime(init_str, input_time_format).strftime(api_time_format)
    end = datetime.datetime.strptime(end_str, input_time_format).strftime(api_time_format)
 
    try:
        # Setting up the headers for the API request
        headers = {'Accept': 'application/json'}
 
        # Constructing the URL for the API request
        url = f'http://gurapi-emergency.guapeton.deep-insight.es/v1/data/data_bydate?projectid=DBEMERGENCY&acqid=unknown&objectid={objectid}&channelid={channelid}&init={init}&end={end}'
 
        # Sending the GET request to the API
        response = requests.get(url, headers=headers)
       
        # Checking if the status code is 200 (OK), if not close the response and return None
        if response.status_code != 200:
            response.close()
            return None
       
        # Returning the JSON content of the response
        return response.json()
   
    except Exception as e:
        # Printing any exception that occurs
        print(f"exception get_data_api_time: {e}")
        if logger:
            logger.error(f"exception get_data_api_time: {e}")
        return None  # Returning None in case of an exception

def fix_units_emergency(id_variable, value):
    """
    Adjusts the sensor data value based on the sensor type identified by `id_variable`.
    
    This function applies a scaling factor (`k`) to the raw sensor data (`value`) depending on the type of sensor identified by `id_variable`. 
    The scaling is necessary to convert raw data into meaningful units that can be interpreted correctly. The function supports a variety of sensors, 
    including temperature, humidity, battery level, gas presence, air quality indices, acceleration, and light intensity among others. 
    Each sensor type has a unique identifier (e.g., "00-temp" for temperature) and an associated scaling factor.
    
    Parameters:
    - id_variable (str): A unique identifier for the sensor type. This identifier is used to determine the scaling factor to be applied to the raw value.
    - value (float or int): The raw data value from the sensor that needs to be adjusted.

    Returns:
    - float: The adjusted sensor data value after applying the appropriate scaling factor.
    """
    # Dictionary of scaling factors
    scale_factors = {
        "00-temp": 0.01, "01-hum": 0.01, "02-bat": 0.01, "03-pg": 1, "02-pres": 0.01,
        "03-siaq": 1, "04-diaq": 1, "Q0-asiaq": 1, "Q1-adiaq": 1, "00-eCO2": 1,
        "01-tvoc": 1, "Q0-calib": 1, "00-accx": 0.001, "01-accy": 0.001, "02-accz": 0.001,
        "00-almtemp": 0.01, "01-almbat": 1, "02-almsiaq": 1, "03-almeco2": 1, "04-almtvoc": 1,
        "00-bat": 0.01, "00-co2": 1, "02-iaq": 1, "Q0-ciaq": 1, "00-pir": 1, "01-lux": 1
    }

    # Apply the scaling factor if the id_variable is in the dictionary
    k = scale_factors.get(id_variable, 1)  # Defaults to 1 if id_variable is not found
    return k * value

    
def fetch_data(
    id_device, 
    id_sensor, 
    id_variable, 
    init_str, 
    end_str, 
    database,
    id_location=np.nan, 
    path_save=None,
    conn_args={},
    logger = None
    ):
    """
    Fetches data for a specified device, sensor, and variable within a given time range, processes it, and optionally saves it locally and/or to a SQL database.

    Parameters:
    - id_device (str): The unique identifier of the device.
    - id_sensor (str): The unique identifier of the sensor.
    - id_variable (str): The unique identifier of the variable being monitored.
    - init_str (str): The start datetime for the data retrieval in 'YYYY-MM-DD HH:MM:SS' format.
    - end_str (str): The end datetime for the data retrieval in 'YYYY-MM-DD HH:MM:SS' format.
    - database: The database connection object or specifier.
    - id_location (float, optional): The location identifier associated with the data. Defaults to np.nan.
    - input_time_format (str, optional): The format of the input time strings. Defaults to '%Y-%m-%d %H:%M:%S'.
    - save_sql (bool, optional): Flag to determine if the data should be saved to a SQL database. Defaults to True.
    - path_save (str, optional): The local file path to save the data as a CSV. If None, the data is not saved locally.
    - conn_args (dict, optional): Additional keyword arguments to pass to SQL functions

    Returns:
    - pandas.DataFrame: A DataFrame containing the fetched data with columns for timestamps, values, device ID, sensor ID, variable ID, and location ID.

    The function first calls an API to retrieve the data, then processes it by converting timestamps to datetime objects and adding identifiers. 
    If 'path_save' is specified, the data is saved to a CSV file. If 'save_sql' is True, the data is saved to a SQL database using the 'write_data' function.
    """
    # Fetching the data from the API
    data = get_data_api_time(
        id_sensor=id_sensor,
        id_beacon=id_device,
        channelid=id_variable,
        init_str=init_str,
        end_str=end_str,
        logger = logger
    )

    df = pd.DataFrame(data)

    df.rename(inplace=True, columns={"time": "timestamp", "data": "value"})
    
    # Converting the time column to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Adding the id_device, id_sensor, and id_variable columns
    df['id_device'] = id_device
    df['id_sensor'] = id_sensor
    df['id_variable'] = f"{id_variable}-{id_sensor}"
    df['id_location'] = id_location
    df["value"] = fix_units_emergency(id_variable, df["value"])

    # Save data to local if path_save is not None
    if path_save:
        df.to_csv(path_save, index=False)

    # The loop is because sometimes the server does not allow many simultaneous connections and since it is thought that
    # this function could be executed concurrently fails until the parallel executions finish
    continue_write_data = True
    while continue_write_data:
        try:
            # Saving the data to a SQL database
            write_data(
                dataframe = df, 
                table_name="data",
                database=database,
                if_exists='append',
                **conn_args
            )
            success_write_data = True
            continue_write_data = False
            print(f"{id_device}-{id_sensor}-{id_variable}: write_data sucess!!!")
            if logger:
                logger.info(f"{id_device}-{id_sensor}-{id_variable}: write_data sucess!!!")
        except Exception as e:
            print(f"{id_device}-{id_sensor}-{id_variable}: write_data exception: {e}")
            if logger:
                logger.error(f"{id_device}-{id_sensor}-{id_variable}: write_data exception: {e}")

        continue_update = True
        while success_write_data and continue_update:
            try:
                print(f"{id_device}-{id_sensor}-{id_variable}: update_value_ssh is working...")
                update_values(
                    table_name="data_last_load",
                    column_to_update="timestamp_last_load",
                    identifier_columns=["id_device", "id_sensor", "id_variable"],
                    # id_variable is in database as "00-temp-sWEA". This is because two different sensors can have the same id_variable
                    identifier_values=[id_device, id_sensor, f"{id_variable}-{id_sensor}"],
                    new_value=end_str,
                    database=database,
                    **conn_args
                )
                continue_update = False
                print(f"{id_device}-{id_sensor}-{id_variable}: update_value sucess!!!")
                if logger:
                    logger.info(f"{id_device}-{id_sensor}-{id_variable}: update_value sucess!!!")
            except Exception as e:
                print(f"{id_device}-{id_sensor}-{id_variable}: write_data eception: {e}")
                if logger:
                    logger.error(f"{id_device}-{id_sensor}-{id_variable}: update_value exception: {e}")

    return df