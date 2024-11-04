import courses_module as cm
import personal as p

# This program will allow you to delete a single entry from either tables in the database

connection = cm.database_connection(p.HOST_NAME, p.USERNAME, p.PASSWORD, cm.DATABASE)

cm.print_list(["course_info", "prerequisite_courses"])
table = int(input("Which table would you like to access?: "))
course_code = input("What is the course code of the entry?: ")

delete_course_query = f"""
DELETE FROM course_info
WHERE
    CourseCode = "{course_code}";
"""

def delete_entry():
    if table == 1:
        query = f"""
        DELETE FROM course_info
        WHERE
            CourseCode = "{course_code}";
        """
        cm.execute_query(connection, query)
    elif table == 2:
        prereq_code = input("What is the corresponding prerequisite code for this entry?: ")
        query = f"""
        DELETE FROM prerequisite_courses
        WHERE
            CourseCode = "{course_code}" AND PrereqCode = "{prereq_code}";
        """
        cm.execute_query(connection, query)
    else:
        return
    return

delete_entry()
