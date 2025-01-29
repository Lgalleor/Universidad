# Sensor Data Collection and Storage System

This project consists of a set of Python scripts designed to fetch sensor data from an API, process it, and store it in a MySQL database. It includes utilities for database interaction, API data retrieval, and the main script to orchestrate the data fetching and storage process.

## Components

The project is divided into several scripts, each serving a specific role:

### 1. `deep_insigth_utils.py`

Provides functions to interact with the DeepInsight API, fetching sensor data based on specified parameters, and processing the data for storage.

- **`get_data_api_time`**: Fetches data from the API based on time range and sensor identifiers.
- **`fix_units_emergency`**: Adjusts sensor data units based on sensor type.
- **`fetch_data`**: Retrieves data for a device, processes it, and stores it in the database.

### 2. `sql_utils.py`

Contains utilities for interacting with MySQL databases, supporting operations like data retrieval, data insertion, and schema management.

- **`get_data`**: Fetches data from a database based on a SQL query.
- **`write_data`**: Writes data to a database table.
- **`update_values`**: Updates specific fields in a database table.
- **`create_db`, `delete_db`**: Manages database creation and deletion.
- **`create_db_schema`, `initialise_db_schema`**: Handles database schema creation and initial data insertion.

### 3. `own_utils.py`

General utility functions, such as loading JSON configuration files.

- **`load_json`**: Loads a JSON file from a specified directory.
- **`execute_concurrently`**: Executes a function concurrently with different sets of arguments, utilizing Python's `concurrent.futures` to perform multiple independent tasks in parallel. 

### 4. `create_db.py`

A script to set up the database by creating its schema and initializing it with predefined data, using configurations defined in external files.

### 5. `main.py`

The main script orchestrates the data fetching and storage process. It supports command-line arguments for specifying execution mode, optional start/end times for data fetching, and allows filtering by database, device, sensor, and variable IDs. This flexibility accommodates automated, scheduled executions as well as ad-hoc data retrieval tasks.

## 6. `measure_database_performance.py`

A script dedicated to evaluating the performance of the MySQL database by executing a predefined set of SQL queries. It measures the execution time, fetches results, and retrieves the execution plan for each query to provide insights into the database's performance under various data retrieval scenarios.

## Setup

To set up the project:

1. Ensure Python 3.6+ is installed.
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure Credentials: Place your database and API credentials in JSON format within the creds directory. Use the provided template files as a guide for the necessary structure.
4. Database Setup: Make sure the MySQL database is created and accessible. Use the create_db.py script if needed to set up the database schema and initial data.
5. Data Fetch Configuration: Define your data fetch settings in a JSON file within the config directory. For example, create data_to_fetch.json. Check structure file if necessary

## Usage

To run the main data collection and storage process:

```bash
python main.py --server [local|server] [--init YYYY-MM-DD HH:MM:SS] [--end YYYY-MM-DD HH:MM:SS] [--database DATABASE_NAME]
```

Example:

```
python main.py --server local --init "2023-01-01 00:00:00" --end "2023-01-10 00:00:00" --database emergency 
```

## Configuration

- **Database and API Credentials**: Store your database and API credentials in JSON format within the `creds` directory. Example files `sql_with_ssh.json` and `sql_without_ssh.json` should be provided as templates.
- **Data Fetch Configuration**: Define the devices and variables for which you wish to fetch data in the `config/data_to_fetch.json` file. This configuration should specify device IDs, sensor IDs, and variable IDs that match your system's setup.

## Logging

Logs are generated to provide insights into the data fetching and storage process, including errors and informational messages. The logging configuration in `main.py` specifies that logs are both printed to the console and written to a file named `logs.log`. This setup helps in monitoring the script's execution and troubleshooting potential issues.

## Contributing

Contributions to this project are welcome. If you have suggestions for improvements or new features, feel free to fork the repository, make your changes, and submit a pull request. Please ensure your code adheres to the existing style and includes appropriate tests and documentation.

## License

This project is licensed under #TODO 

## Acknowledgments

We extend our heartfelt gratitude to the individuals whose contributions have significantly enriched this project:

- **Robert Novak**
- **Marcos Delgado**


## Troubleshooting

#TODO

## Last Updated

This README was last updated on February 7, 2024.

Please note that the project itself may have been updated since then. For the most recent changes, check the commit history or the project's update logs.
