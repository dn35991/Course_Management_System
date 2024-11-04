import courses_module as cm
import personal as p

# This program will initialize the database using the specified names in the course_module.py module.
#   Only run this file once to initialize the database and tables.

server_connection = cm.server_connection(p.HOST_NAME, p.USERNAME, p.PASSWORD)

database_query = f"""
CREATE DATABASE {cm.DATABASE};
"""

course_table_query = """
CREATE TABLE course_info (
    CourseCode VARCHAR(30) NOT NULL,
    CourseName VARCHAR(10000),
    Credits DECIMAL(10,2),
    CourseType VARCHAR(20),
    Completion VARCHAR(20),
    Term VARCHAR(5),
    Grade INT,
    PRIMARY KEY (CourseCode)
);
"""

prereq_table_query = """
CREATE TABLE prerequisite_courses (
    CourseCode VARCHAR(30) NOT NULL,
    PrereqCode VARCHAR(30),
    MinGrade INT
);
"""

cm.execute_query(server_connection, database_query)

database_connection = cm.database_connection(p.HOST_NAME, p.USERNAME, p.PASSWORD, cm.DATABASE)

cm.execute_query(database_connection, course_table_query)
cm.execute_query(database_connection, prereq_table_query)