import courses_module as cm
import personal as p
import queries as q
import pandas as pd

# This program will allow you to view a specifc table with every single column and row

connection = cm.database_connection(p.HOST_NAME,p.USERNAME, p.PASSWORD, p.DATABASE)

course_info_table_query = f"""
SELECT *
FROM 
    course_info AS C
ORDER BY 
    {q.ORDERING};
"""

prereq_info_table_query = f"""
SELECT 
	PC.CourseCode AS CourseCode,
    PC.PrereqCode AS PrereqCode,
    PC.MinGrade AS MinGrade
FROM 
	prerequisite_courses as PC
INNER JOIN
	course_info as C
ON
	C.CourseCode = PC.CourseCode
ORDER BY
    {q.ORDERING};
"""

plan_table_query = f"""
SELECT 
    P.*
FROM
    academic_plan AS P
INNER JOIN
    course_info AS C
ON
    C.CourseCode = P.CourseCode
ORDER BY
    {q.ORDERING}
"""
cm.print_list(["course_info", "prerequisite_courses", "academic_plan"])
table_name = int(input(f"Which table would you like to view?: "))

table = []

def read_table():
    if table_name == 1:
        cm.display_info(connection, course_info_table_query, cm.COURSE_COLUMNS, table)
    elif table_name == 2:
        cm.display_info(connection, prereq_info_table_query, cm.PREREQ_COLUMNS, table)
    elif table_name == 3:
        cm.display_info(connection, plan_table_query, cm.PLAN_COLUMNS, table)
    else:
        return
    return

read_table()