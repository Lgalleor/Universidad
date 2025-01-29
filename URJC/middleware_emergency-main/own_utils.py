"""
This module provides general utility functions that are commonly used across different parts of an application. 
The utilities included here are designed to streamline common tasks such as file handling and data parsing. 
Currently, the module includes the following function:

1. `load_json`: Loads and parses a JSON file from a specified directory. This function is particularly useful for reading 
configuration files, such as database connection settings or API keys. It ensures that the path to the JSON file is correctly
constructed and normalized, regardless of the operating system, and returns the content as a Python dictionary.

2. `execute_concurrently`: Executes a function concurrently with different sets of arguments. This function is useful for
performing multiple independent tasks in parallel, such as making API requests to different endpoints or processing multiple
files simultaneously. It uses Python's concurrent.futures module to create a ThreadPoolExecutor and submit the function with
different sets of arguments as concurrent tasks. The results are collected and returned as a list.

The function within this module is designed to be reusable and easy to integrate into various parts of an application, 
promoting code reuse and modular design.

"""

import json
import os
import concurrent.futures


def load_json(preceding_path, file_name):
    """
    Loads a JSON file containing json from a specified directory.

    This function is particularly useful for loading credential files, such as database
    configurations, API keys, etc. It combines the preceding path and file name to form
    a full path, normalizes it, and then loads the JSON content into a dictionary.

    Parameters:
    preceding_path (str): The directory path preceding the file name.
    file_name (str): The name of the JSON file to be loaded without extension

    Returns:
    dict: A dictionary containing the data from the JSON file.

    Example:
    >>> credentials = load_json("creds", "credentials")
    >>> print(credentials)
    """

    # Construct the full file path and normalize it
    full_path = os.path.normpath(os.path.join(preceding_path, f"{file_name}.json"))

    # Load and return the JSON content
    with open(full_path, 'r') as json_file:
        return json.load(json_file)

#TODO: Investigar por qué no funcionan los logs cuando se ejecutan concurrentemente y solucionarlo 
def execute_concurrently(func, args_list, logger=None):
    """
    Executes a function concurrently with different sets of arguments.
    
    Parameters:
    - func (callable): A callable object (e.g., function) to be executed.
    - args_list (list): A list of dictionaries, where each dictionary contains the keyword arguments for the function.
    - logger (logging.Logger, optional): A logger object for logging messages. Defaults to None.
    
    Returns:
    - list: A list of results from the function.
    
    Example:
    >>> def add(x, y):
    ...     return x + y
    ...
    >>> args_list = [{'x': 5, 'y': 3}, {'x': 10, 'y': 7}]
    >>> execute_concurrently(add, args_list)
    [8, 17]
    """
    
    # Initialize an empty list to store the results
    results = []
    
    # Create a ThreadPoolExecutor to manage the concurrent execution of the function
    with concurrent.futures.ThreadPoolExecutor() as executor:
        
        # Create a list to store the Future objects returned by executor.submit,
        # and map each Future to its corresponding arguments
        futures = {executor.submit(func, **args): args for args in args_list}
        
        # Iterate through the Future objects as they complete
        for future in concurrent.futures.as_completed(futures):
            args = futures[future]
            try:
                # Get the result of the completed function
                result = future.result()
                
                # Log success message if logger is provided
                if logger:
                    logger.info(f"Task with args {args} processed successfully.")
                
                results.append(result)
            except Exception as exc:
                # Log exception message if logger is provided
                if logger:
                    logger.error(f"Task with args {args} generated an exception: {exc}")
                
                results.append(exc)
    
    # Return the list of results
    return results