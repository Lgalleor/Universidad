"""
This module provides utility functions for database operations including data retrieval, writing, and updates, 
as well as database and schema management. It supports direct database connections as well as connections via SSH tunneling 
for enhanced security. The module is designed to work with MySQL databases and includes the following key functionalities:

1. `get_data`: Fetches data from a specified MySQL database by executing a given SQL query. It supports optional SSH tunneling 
for secure remote database access.

2. `write_data`: Writes data from a pandas DataFrame to a specified table in a MySQL database. It allows for flexible 
data insertion policies and also supports SSH tunneling.

3. `update_values`: Updates specific fields in a database table, identified by a set of conditions. This function is useful 
for maintaining the latest state of data records in the database.

4. `create_db`: Creates a new MySQL database if it doesn't already exist, using an existing database connection.

5. `delete_db`: Deletes an entire MySQL database, including all its tables and data, optionally using SSH tunneling for access.

6. `create_db_schema`: Creates tables within a database based on a provided schema definition. This function is essential 
for initializing databases with the required structure for data storage.

7. `initialise_db_schema`: Populates database tables with initial data based on provided SQL insert statements. 
This function is useful for setting up a database with initial data sets.

8. `measure_query_execution_time`: Measures the execution time of SQL queries, fetches the results, and retrieves the execution 
plan, aiding in query performance analysis.

9. `run_performance_tests`: Executes a series of SQL queries to evaluate their performance on a MySQL database, 
optionally through SSH tunneling. This function returns a DataFrame summarizing the performance metrics of each query.

The module is designed to be flexible and robust, handling errors gracefully and ensuring database operations are performed 
securely and efficiently.
"""
import time
import sshtunnel
import pymysql
import pandas as pd
from sqlalchemy import create_engine
import datetime
import requests

from own_utils import load_json

def get_data(query, db_user, db_password, database, db_server='127.0.0.1', ssh_host=None, ssh_port=None, ssh_user=None, ssh_password=None):
    """
    Fetch data from a MySQL database, optionally through an SSH tunnel.

    Parameters:
    query (str): SQL query to execute.
    db_user (str): Username for database access.
    db_password (str): Password for database access.
    database (str): Name of the database to query.
    db_server (str, optional): Address of the database server. Defaults to '127.0.0.1' (local).
    ssh_host (str, optional): Address of the SSH server for tunneling. Defaults to None.
    ssh_port (int, optional): Port of the SSH server for tunneling. Defaults to None.
    ssh_user (str, optional): Username for SSH access. Defaults to None.
    ssh_password (str, optional): Password for SSH access. Defaults to None.

    Returns:
    DataFrame: A pandas DataFrame containing the query results, or None in case of an error.
    """
    tunnel = None
    try:
        if ssh_host and ssh_port and ssh_user and ssh_password:
            # Establish an SSH tunnel
            tunnel = sshtunnel.SSHTunnelForwarder(
                (ssh_host, ssh_port),
                ssh_username=ssh_user,
                ssh_password=ssh_password,
                remote_bind_address=(db_server, 3306)
            )
            tunnel.start()
            conn_params = {
                'host': '127.0.0.1',
                'port': tunnel.local_bind_port,
                'user': db_user,
                'passwd': db_password,
                'db': database
            }
        else:
            # Direct connection to the database
            conn_params = {
                'host': db_server,
                'user': db_user,
                'passwd': db_password,
                'db': database
            }

        # Establishing the database connection
        with pymysql.connect(**conn_params) as _db:
            with _db.cursor() as _cursor:
                data = pd.read_sql(query, _db)
                return data

    except Exception as e:
        print(f"Exception in get_data: {e}")
        return None
    finally:
        if tunnel:
            tunnel.close()

def write_data(
    dataframe,
    table_name,
    db_user,
    db_password,
    database,
    db_server='127.0.0.1',
    if_exists='fail',
    ssh_host=None,
    ssh_port=None,
    ssh_user=None,
    ssh_password=None
    ):
    """
    Write data to a MySQL database table, optionally through an SSH tunnel.

    Parameters:
    dataframe (DataFrame): pandas DataFrame containing the data to write.
    table_name (str): Name of the database table to write to.
    db_user (str): Username for database access.
    db_password (str): Password for database access.
    database (str): Name of the database.
    db_server (str, optional): Address of the database server. Defaults to '127.0.0.1'.
    if_exists (str, optional): Behavior when the table already exists. Defaults to 'fail'.
    ssh_host (str, optional): Address of the SSH server for tunneling. Defaults to None.
    ssh_port (int, optional): Port of the SSH server for tunneling. Defaults to None.
    ssh_user (str, optional): Username for SSH access. Defaults to None.
    ssh_password (str, optional): Password for SSH access. Defaults to None.
    """
    try:

        if ssh_host and ssh_port and ssh_user and ssh_password:
            # Establish an SSH tunnel
            tunnel = sshtunnel.SSHTunnelForwarder(
                (ssh_host, ssh_port),
                ssh_username=ssh_user,
                ssh_password=ssh_password,
                remote_bind_address=(db_server, 3306)
            )
            tunnel.start()
            connection_string = f"mysql+pymysql://{db_user}:{db_password}@127.0.0.1:{tunnel.local_bind_port}/{database}"
        else:
            # Direct connection string
            connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_server}/{database}"
            tunnel = False

        # Create SQLAlchemy engine and write the DataFrame to the SQL table
        engine = create_engine(connection_string)
        dataframe.to_sql(table_name, engine, if_exists=if_exists, index=False)

    except Exception as e:
        print(f"Exception in write_data: {e}")
    finally:
        if tunnel:
            tunnel.close()


def update_values(
    table_name,
    column_to_update,
    new_value,
    identifier_columns,
    identifier_values,
    db_user,
    db_password,
    database,
    db_server='127.0.0.1',
    ssh_host=None,
    ssh_port=None,
    ssh_user=None,
    ssh_password=None
):
    """
    Update values in a MySQL database table, optionally through an SSH tunnel.

    Parameters:
    table_name (str): Name of the database table to update.
    column_to_update (str): Name of the column to update.
    new_value: New value for the column to update.
    identifier_columns (list): List of columns to identify the row to update.
    identifier_values (list): List of values corresponding to the identifier columns.
    db_user (str): Username for database access.
    db_password (str): Password for database access.
    database (str): Name of the database.
    db_server (str, optional): Address of the database server. Defaults to '127.0.0.1'.
    ssh_host (str, optional): Address of the SSH server for tunneling. Defaults to None.
    ssh_port (int, optional): Port of the SSH server for tunneling. Defaults to None.
    ssh_user (str, optional): Username for SSH access. Defaults to None.
    ssh_password (str, optional): Password for SSH access. Defaults to None.
    """
    tunnel = None
    connection = None
    try:
        if ssh_host and ssh_port and ssh_user and ssh_password:
            # Establish an SSH tunnel
            tunnel = sshtunnel.SSHTunnelForwarder(
                (ssh_host, ssh_port),
                ssh_username=ssh_user,
                ssh_password=ssh_password,
                remote_bind_address=(db_server, 3306)
            )
            tunnel.start()
            connection = pymysql.connect(host='127.0.0.1',
                                         user=db_user,
                                         password=db_password,
                                         port=tunnel.local_bind_port,
                                         database=database)
        else:
            # Direct connection
            connection = pymysql.connect(host=db_server,
                                         user=db_user,
                                         password=db_password,
                                         database=database)

        with connection.cursor() as cursor:
            where_conditions = " AND ".join([f"{col} = %s" for col in identifier_columns])
            update_query = f"""UPDATE {table_name}
                               SET {column_to_update} = %s
                               WHERE {where_conditions}"""
            query_params = [new_value] + identifier_values
            cursor.execute(update_query, query_params)
            connection.commit()

    except Exception as e:
        print(f"Exception in update_values: {e}")
    finally:
        if connection:
            connection.close()
        if tunnel:
            tunnel.close()


def create_db(connection, database_name):
    """
    Create a database if it does not exist, using an existing database connection.

    Parameters:
    connection: An existing database connection object.
    database_name (str): Name of the database to create.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        # Ensure the connection is committed if necessary
        connection.commit()
    except Exception as e:
        print(f"Exception in create_db: {e}")


def delete_db(
        db_user, 
        db_password, 
        database, 
        db_server='127.0.0.1', 
        ssh_host=None, 
        ssh_port=None, 
        ssh_user=None, 
        ssh_password=None):
    """
    Delete the specified database and all of its tables.

    Parameters:
    db_user (str): Username for database access.
    db_password (str): Password for database access.
    database (str): Name of the database to delete.
    db_server (str, optional): Address of the database server. Defaults to '127.0.0.1'.
    ssh_host (str, optional): Address of the SSH server for tunneling. Defaults to None.
    ssh_port (int, optional): Port of the SSH server for tunneling. Defaults to None.
    ssh_user (str, optional): Username for SSH access. Defaults to None.
    ssh_password (str, optional): Password for SSH access. Defaults to None.
    """
    # Setup SSH tunnel if needed
    tunnel = None
    if ssh_host and ssh_port and ssh_user and ssh_password:
        tunnel = sshtunnel.SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_password=ssh_password,
            remote_bind_address=(db_server, 3306)
        )
        tunnel.start()
        connection = pymysql.connect(host='127.0.0.1', user=db_user, password=db_password, port=tunnel.local_bind_port)
    else:
        connection = pymysql.connect(host=db_server, user=db_user, password=db_password)

    try:
        with connection.cursor() as cursor:
            # Drop the database
            cursor.execute(f"DROP DATABASE IF EXISTS `{database}`;")
        connection.commit()
    except Exception as e:
        pass
    finally:
        if connection:
            connection.close()
        if tunnel:
            tunnel.stop()

def create_db_schema(
        db_user, 
        db_password, 
        database, 
        db_schema,
        db_server='127.0.0.1', 
        ssh_host=None, 
        ssh_port=None, 
        ssh_user=None, 
        ssh_password=None):
    """
    Create the database schema (if not exists) based on the provided dictionary of SQL commands.

    Parameters:
    db_user (str): Username for database access.
    db_password (str): Password for database access.
    database (str): Name of the database to create and use.
    db_schema (dict): Dictionary containing table names as keys and SQL create statements as values.
    db_server (str, optional): Address of the database server. Defaults to '127.0.0.1'.
    ssh_host (str, optional): Address of the SSH server for tunneling. Defaults to None.
    ssh_port (int, optional): Port of the SSH server for tunneling. Defaults to None.
    ssh_user (str, optional): Username for SSH access. Defaults to None.
    ssh_password (str, optional): Password for SSH access. Defaults to None.
    """

    tunnel = None
    if ssh_host and ssh_port and ssh_user and ssh_password:
        tunnel = sshtunnel.SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_password=ssh_password,
            remote_bind_address=(db_server, 3306)
        )
        tunnel.start()
        connection = pymysql.connect(host='127.0.0.1', user=db_user, password=db_password, port=tunnel.local_bind_port)
    else:
        connection = pymysql.connect(host=db_server, user=db_user, password=db_password)

    try:
        create_db(connection, database)
        connection.select_db(database)

        with connection.cursor() as cursor:
            for table_name, sql_command in db_schema.items():
                try:
                    cursor.execute(sql_command)
                    print(f"{table_name} created successfully.")
                except Exception as e:
                    print(f"Exception creating {table_name}: {e}")
        connection.commit()
    except Exception as e:
        print(f"Exception in create_db_schema: {e}")
    finally:
        if connection:
            connection.close()
        if tunnel:
            tunnel.stop()

def initialise_db_schema(
        db_user, 
        db_password, 
        database, 
        db_data,
        db_server='127.0.0.1', 
        ssh_host=None, 
        ssh_port=None, 
        ssh_user=None, 
        ssh_password=None):
    """
    Initialize the database with data based on the provided dictionary of SQL insert commands.

    Parameters:
    db_user (str): Username for database access.
    db_password (str): Password for database access.
    database (str): Name of the database to populate with data.
    db_data (dict): Dictionary containing table names as keys and SQL insert statements as values.
    db_server (str, optional): Address of the database server. Defaults to '127.0.0.1'.
    ssh_host (str, optional): Address of the SSH server for tunneling. Defaults to None.
    ssh_port (int, optional): Port of the SSH server for tunneling. Defaults to None.
    ssh_user (str, optional): Username for SSH access. Defaults to None.
    ssh_password (str, optional): Password for SSH access. Defaults to None.
    """

    tunnel = None
    if ssh_host and ssh_port and ssh_user and ssh_password:
        tunnel = sshtunnel.SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_password=ssh_password,
            remote_bind_address=(db_server, 3306)
        )
        tunnel.start()
        connection = pymysql.connect(host='127.0.0.1', user=db_user, password=db_password, port=tunnel.local_bind_port)
    else:
        connection = pymysql.connect(host=db_server, user=db_user, password=db_password)

    try:
        connection.select_db(database)

        with connection.cursor() as cursor:
            for table_name, sql_command in db_data.items():
                if sql_command:  # Ensure the command is not empty
                    try:
                        cursor.execute(sql_command)
                        print(f"Data inserted into {table_name} successfully.")
                    except Exception as e:
                        print(f"Exception inserting data into {table_name}: {e}")
        connection.commit()
    except Exception as e:
        print(f"Exception in initialise_db_schema: {e}")
    finally:
        if connection:
            connection.close()
        if tunnel:
            tunnel.stop()

def measure_query_execution_time(cursor, query):
    """
    Measures the execution time of a SQL query, fetches its results, and retrieves its execution plan.

    This function executes the provided SQL query using the given cursor, measures the execution time, fetches all the results, and captures the execution plan using the EXPLAIN statement. The information is returned in a dictionary. If an error occurs during query execution or result fetching, the function logs the error and returns default values in the dictionary.

    Parameters:
    - cursor (Cursor): A database cursor object, used to execute the query and fetch results.
    - query (str): The SQL query string to be executed.

    Returns:
    - dict: A dictionary containing the following keys:
        - 'results': A list of tuples containing the query results.
        - 'execution_time': The time taken to execute the query and fetch results, measured in seconds.
        - 'explain_plan': A list of tuples containing the execution plan of the query.
        - 'start_time': The timestamp marking the start of the query execution.
        - 'end_time': The timestamp marking the end of the query execution.
        - 'error': An error message if an error occurred during query execution, otherwise None.

    The function aims to provide detailed insights into the performance of SQL queries, including their efficiency and potential bottlenecks.
    """
    result_dict = {
        'results': [],
        'execution_time': 0,
        'explain_plan': [],
        'start_time': 0,
        'end_time': 0,
        'error': None
    }

    try:
        result_dict['start_time'] = time.time()  # Start timer before query execution
        
        # Obtener el plan de ejecución
        cursor.execute(f"EXPLAIN {query}")
        result_dict['explain_plan'] = cursor.fetchall()

        # Ejecutar la consulta original
        cursor.execute(query)
        result_dict['results'] = cursor.fetchall()
        
        result_dict['end_time'] = time.time()  # End timer after fetching results
        result_dict['execution_time'] = result_dict['end_time'] - result_dict['start_time']  # Calculate execution time
        
    except Exception as e:
        result_dict['error'] = f"Error executing query: {e}"
        print(result_dict['error'])
    
    return result_dict


def run_performance_tests(query_list, db_user, db_password, database, db_server='127.0.0.1', ssh_host=None, ssh_port=None, ssh_user=None, ssh_password=None):
    """
    Executes a list of SQL queries to measure their performance on a MySQL database, optionally through an SSH tunnel.

    Parameters:
    - query_list (list of str): List of SQL queries to be executed for performance measurement.
    - db_user (str): Username for database access.
    - db_password (str): Password for database access.
    - database (str): Name of the database where queries will be executed.
    - db_server (str, optional): Address of the database server. Defaults to '127.0.0.1' (local).
    - ssh_host (str, optional): Address of the SSH server for tunneling. Defaults to None.
    - ssh_port (int, optional): Port of the SSH server for tunneling. Defaults to None.
    - ssh_user (str, optional): Username for SSH access. Defaults to None.
    - ssh_password (str, optional): Password for SSH access. Defaults to None.

    Returns:
    - pandas.DataFrame: A DataFrame containing the performance summary of each query, including execution times and other relevant metrics, or None in case of an error.
    """
    tunnel = None
    summary = []

    try:
        if ssh_host and ssh_port and ssh_user and ssh_password:
            # Establish an SSH tunnel
            tunnel = sshtunnel.SSHTunnelForwarder(
                (ssh_host, ssh_port),
                ssh_username=ssh_user,
                ssh_password=ssh_password,
                remote_bind_address=(db_server, 3306)
            )
            tunnel.start()
            conn_params = {
                'host': '127.0.0.1',
                'port': tunnel.local_bind_port,
                'user': db_user,
                'passwd': db_password,
                'db': database
            }
        else:
            # Direct connection to the database
            conn_params = {
                'host': db_server,
                'user': db_user,
                'passwd': db_password,
                'db': database
            }

        # Establishing the database connection
        db_conn = pymysql.connect(**conn_params)
        cursor = db_conn.cursor()

        # Execute each query and measure performance
        for query in query_list:
            result_dict = measure_query_execution_time(cursor, query)
            summary.append({
                'Query': query,
                'Rows': len(result_dict['results']),
                'Columns': len(result_dict['results'][0]) if result_dict['results'] else 0,
                'Execution Time (s)': result_dict['execution_time'],
                'Explain Plan': result_dict['explain_plan'],
                'Start Time': result_dict['start_time'],
                'End Time': result_dict['end_time'],
                'Error': result_dict['error']
            })

        db_conn.close()

    except Exception as e:
        print(f"Exception in run_performance_tests: {e}")
        return None

    finally:
        if tunnel:
            tunnel.close()

    # Convert the summary list to a pandas DataFrame for analysis
    summary_df = pd.DataFrame(summary)
    return summary_df

