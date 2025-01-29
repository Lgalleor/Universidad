"""
This script automates the process of setting up a new database named "emergency" by creating its schema and initializing it with 
predefined data. It leverages utility functions from 'own_utils.py' and 'sql_utils.py' to achieve this.

First, the script loads database credentials and SSH tunneling details (if needed) from a JSON file using the 'load_json' 
function from 'own_utils'. Then, it uses 'create_db_schema' and 'initialise_db_schema' functions from 'sql_utils' to create the 
database schema and populate it with initial data, respectively.

The schema and initial data are defined in external configuration files located within the 'config.sql_queries' package. 
'db_schema' contains the SQL commands for creating tables and defining their structure, while 'db_data' provides the SQL insert 
statements to populate these tables with initial records.

This script is typically run as a one-time setup operation to prepare the database for use by the application.

Usage:
- Ensure that the database credentials file is present and correctly formatted.
- Run this script to create and initialize the 'emergency' database.

Note: This script should be used with caution, as it can lead to data loss if run on an existing database with the same name.
"""
from own_utils import load_json
from sql_utils import create_db_schema, delete_db, initialise_db_schema
from config.sql_queries.emergency_schema import db_schema
from config.sql_queries.initialise_emergency_schema import db_data

creds_sql = load_json("creds","sql_with_ssh")

create_db_schema(database = "emergency", db_schema= db_schema, **creds_sql)
initialise_db_schema(database = "emergency", db_data = db_data, **creds_sql)