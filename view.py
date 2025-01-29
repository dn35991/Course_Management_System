import courses_module as cm
import personal as p
import queries as q

# This program will allow you to view the database based on differnet variables 

connection = cm.database_connection(p.HOST_NAME, p.USERNAME, p.PASSWORD, p.DATABASE)
view_options = [
    "Course Type", 
    "Completion Type", 
    "Term", 
    "Grade", 
    "Course Code", 
    "Prerequisite Course Code", 
    "Prerequisite Required Courses",
    "Course Prerequisites"]

cm.print_list(view_options)
view = int(input("What would you like to view?: "))
option = 0

def column_except1_list(column):
    result = []
    i = 0
    while i < len(cm.COURSE_COLUMNS):
        if i == column:
            i = i + 1
            continue    
        else:
            result.append(cm.COURSE_COLUMNS[i])
            i = i + 1
    return result

def course_query(column):
    if column == 1 or column == 2:
        column_name = cm.COURSE_COLUMNS[column + 2]
        cm.print_list(cm.dict_value(cm.COURSE_DICT, column + 2))
        item = int(input(f"What {view_options[column - 1].lower()} would you like to view?: "))
        query = f"""
        SELECT
            {cm.list_to_string(column_except1_list(column + 2), ", ")}
        FROM
            course_info AS C
        WHERE 
            {column_name} = "{cm.COURSE_DICT[column_name][item - 1]}"
        ORDER BY
            {q.ORDERING}
        """
    elif column == 3:
        column_name = cm.COURSE_COLUMNS[column + 2]
        item = input(f"Which {view_options[column - 1].lower()} would you like to view?: ")
        query = f"""
        SELECT
            {cm.list_to_string(column_except1_list(column + 2), ", ")}
        FROM
            course_info AS C
        WHERE 
            {column_name} = "{item}"
        ORDER BY
            {q.ORDERING}
        """
    elif column == 4:
        column_name = cm.COURSE_COLUMNS[6]
        low_bound = int(input("What is the lowest bounded grade?: "))
        high_bound = int(input("What is the highest bounded grade?: "))
        query = f"""
        SELECT *
        FROM
            course_info AS C
        WHERE 
            {column_name} >= {low_bound} AND {column_name} <= {high_bound}
        ORDER BY
            {q.ORDERING}
        """
    elif column == 5:
        column_name = cm.COURSE_COLUMNS[0]
        course_code = input("What course code (not exact code) are you viewing?: ")
        query = f"""
        SELECT *
        FROM
            course_info AS C
        WHERE 
            {column_name} LIKE "%{course_code}%"
        ORDER BY
            {q.ORDERING}
        """
    else:    
        return
    
    return query

def prereq_query():
    course_code = input("What prerequisite course would you like to view?: ")
    query = f"""
    SELECT *
    FROM
        prerequisite_courses AS P
    WHERE 
        {cm.PREREQ_COLUMNS[1]} LIKE "%{course_code}%";
    """
    return query

def course_prereqs():
    course_code = input("What course code would you like to view?: ")
    query = f"""
    SELECT *
    FROM
        prerequisite_courses
    WHERE 
        CourseCode LIKE "%{course_code}%";
    """
    return query

table = []

def views():
    if 1 <= view <= 3:
        query = course_query(view)
        cm.display_info(connection, query, column_except1_list(view + 2), table)
    elif 4 <= view <= 5:
        query = course_query(view)
        cm.display_info(connection, query, cm.COURSE_COLUMNS, table)
    elif view == 6:
        query = prereq_query()
        cm.display_info(connection, query, cm.PREREQ_COLUMNS, table)
    elif view == 7:
        cm.display_info(connection, q.PREREQS, q.COLUMNS_1, table)
    elif view == 8:
        query = course_prereqs()
        cm.display_info(connection, query, cm.PREREQ_COLUMNS, table)
    else:
        return
    return

views()