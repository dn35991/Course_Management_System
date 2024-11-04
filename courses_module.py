import mysql.connector
from mysql.connector import Error
import pandas as pd
from IPython.display import display

# This is the module used in all of the programs for this project. The global constants should not be changed
#   since the database is initialized with specific column and table names. Before begining to run any programs, 
#   make sure to edit the file "personal.py" where you must enter the values for "HOST_NAME", "USERNAME", and "PASSWORD"

DATABASE = "courses"
COURSE_TABLE = "course_info"
PREREQ_TABLE = "prerequisite_courses"

COURSE_DICT = {
    "CourseCode": None,
    "CourseName": None,
    "Credits": None,
    "CourseType": ["Math", "Non-Math", "PD"],
    "Completion": ["Completed", "Current", "Planned", "Available", "Prereq"],
    "Term": None,
    "Grade": None
}

PREREQ_DICT = {
    "CourseCode": None,
    "PrereqCode": None,
    "MinGrade": None
}

COURSE_COLUMNS = list(COURSE_DICT.keys())
PREREQ_COLUMNS = list(PREREQ_DICT.keys())
COMPLETION_TYPES = COURSE_DICT[list(COURSE_DICT.keys())[4]]
COURSE_TYPE = COURSE_DICT[list(COURSE_DICT.keys())[3]]

def server_connection(host_name, username, password):
    connection = None
    try: 
        connection = mysql.connector.connect(
            host = host_name,
            user = username,
            passwd = password
        )
        print("MySQL Database Connection Successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

def database_connection(host_name, username, password, database_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = username,
            passwd = password,
            database = database_name,
            autocommit = True
        )
        print("MySQL Database Connection Successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit
        print("Query Successful")
    except Error as err:
        print(f"Error: '{err}'")

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def display_info(connection, info_query, column_names, table):
    results = read_query(connection, info_query)
    for data in results:
        data = list(data)
        table.append(data)
    return display(pd.DataFrame(table, columns = column_names))

def dict_value(dict, index):
    return dict[list(dict.keys())[index]]

def print_list(item):
    i = 1
    if type(item) is not list:
        return
    else:
        for value in item:
            print(f"{i}. {value}")
            i = i + 1
        return

def list_to_string(list, seperator):
    result = f"{seperator}".join(list)
    return result
