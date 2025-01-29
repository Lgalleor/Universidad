"""
This script, `measure_database_performance.py`, is designed to conduct comprehensive performance testing on a MySQL database
by executing a series of predefined SQL queries. The queries are crafted to simulate various real-world data retrieval scenarios,
ranging from simple data fetches based on time intervals to more complex queries involving multiple filters and aggregation functions.
The script employs the `run_performance_tests` function from the `sql_utils` module to measure and record the performance of each query.

The script follows these steps:

1. Load SQL credentials, including SSH details if required, for secure database access.

2. Define an extensive list of SQL queries, tailored to test different aspects of database performance. 

3. Execute the performance tests using the `run_performance_tests` function, which measures execution time, fetches results, 
and retrieves execution plans for each query.

4. Save the performance metrics, including execution times and other relevant details, to a CSV file. The filename is timestamped 
to ensure uniqueness and traceability.

The script is intended for database administrators and developers who need to assess the performance impact of various query 
patterns on their MySQL databases. It facilitates identifying potential bottlenecks and optimizing database and query performance.


"""
import datetime
import os
from own_utils import load_json
from sql_utils import run_performance_tests

# Load SQL credentials with SSH
creds_sql = load_json("creds", "sql_with_ssh")

# Extensive list of queries for performance testing
query_list = [
    # Queries increasing one week by timestamp
    "SELECT * FROM data WHERE timestamp BETWEEN '2024-02-01' AND '2024-02-8';",
    "SELECT * FROM data WHERE timestamp BETWEEN '2024-02-01' AND '2024-02-15';",
    "SELECT * FROM data WHERE timestamp BETWEEN '2024-02-01' AND '2024-02-23';",
    "SELECT * FROM data WHERE timestamp BETWEEN '2024-02-01' AND '2024-02-28';",
    # Queries in 1 month increasing filters with variables which have indexes (device with 60 seconds rate)
    "SELECT * FROM data WHERE timestamp BETWEEN '2024-02-01' AND '2024-02-28' AND id_device = 'DBEM009';",
    "SELECT * FROM data WHERE timestamp BETWEEN '2024-02-01' AND '2024-02-28' AND id_device = 'DBEM009' AND id_sensor = 'sWEA' AND id_variable = '00-temp-sWEA';",
    # Queries in 1 month increasing filters with variables which have indexes (device with 30 seconds rate)
    "SELECT * FROM data WHERE timestamp BETWEEN '2024-02-01' AND '2024-02-28' AND id_device = 'DBEM010';",
    "SELECT * FROM data WHERE timestamp BETWEEN '2024-02-01' AND '2024-02-28' AND id_device = 'DBEM010' AND id_sensor = 'sWEA' AND id_variable = '00-temp-sWEA';",
    # Queries in 1 month increasing filters with variables which have indexes (device with 60 seconds rate)
    "SELECT * FROM data WHERE timestamp BETWEEN '2024-02-01' AND '2024-02-28' AND id_device = 'DBEM002';",
    "SELECT * FROM data WHERE timestamp BETWEEN '2024-02-01' AND '2024-02-28' AND id_device = 'DBEM002' AND id_sensor = 'sWEA' AND id_variable = '00-temp-sWEA';",
    # Queries using group by COUNT increasing complexity of filter (before and after groupby)
    "SELECT id_device, COUNT(*) FROM data WHERE timestamp >= '2024-02-01' AND timestamp <= '2024-02-28' GROUP BY id_device;",
    "SELECT id_device, COUNT(*) FROM data WHERE timestamp >= '2024-02-01' AND timestamp <= '2024-02-28' AND id_sensor = 'sWEA' GROUP BY id_device;",
    "SELECT id_device, COUNT(*) FROM data WHERE timestamp >= '2024-02-01' AND timestamp <= '2024-02-28' AND id_sensor = 'sWEA' AND id_variable = '00-temp-sWEA' GROUP BY id_device;",
    "SELECT id_device, COUNT(*) FROM data WHERE timestamp >= '2024-02-01' AND timestamp <= '2024-02-28' AND id_sensor = 'sWEA' AND id_variable = '00-temp-sWEA' HAVING COUNT(*) > 10 GROUP BY id_device;",
    # Queries using group by AVG increasing complexity of filter (before and after groupby)
    "SELECT id_device, AVG(value) FROM data WHERE timestamp BETWEEN '2024-02-01' AND '2024-03-01' GROUP BY id_device AND id_variable = '00-temp-sWEA';",
]

# Run performance tests
summary_df = run_performance_tests(query_list, database = "emergency", **creds_sql)

# Ensure the directory exists
output_dir = "database_performance_metrics/"
os.makedirs(output_dir, exist_ok=True)

# Generate a filename based on the current datetime
filename = datetime.datetime.now().strftime("%Y_%m_%d %H_%M_%S") + ".csv"

# Save the summary DataFrame to a CSV file
summary_df.to_csv(os.path.join(output_dir, filename), index=False, sep="\t")