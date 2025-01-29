import courses_module as cm
import personal as p

# This program will allow you to update the entire system after a recent change in the 
#   completion status of courses

connection = cm.database_connection(p.HOST_NAME, p.USERNAME, p.PASSWORD, p.DATABASE)
courses_query = """
SELECT
    CourseCode
FROM
    course_info
WHERE
    Completion = "Available" OR
    Completion = "Prereq";
"""

courses = []
num_prereqs = []
view = []
def update_all():
    cm.data_list(connection, courses_query, ["Courses"], courses)
    for elem in courses:
        num_prereqs = []
        code = str(elem[0])
        prereqs = f"""
        SELECT 
            COUNT(PrereqCode)
        FROM 
            prerequisite_courses
        WHERE 
            CourseCode = "{code}" AND
            PrereqCode IN
                (SELECT
                    CourseCode
                FROM
                    course_info
                WHERE 
                    Completion = "Planned" OR
                    Completion = "Available" OR
                    Completion = "Prereq");
        """
        cm.data_list(connection, prereqs, ["Number"], num_prereqs)
        
        if int(num_prereqs[0][0]) == 0:
            query = f"""
            UPDATE 
                course_info
            SET Completion = "Available"
            WHERE CourseCode = "{code}";
            """
            cm.execute_query(connection, query) 
        else:
            query = f"""
            UPDATE 
                course_info
            SET Completion = "Prereq"
            WHERE CourseCode = "{code}";
            """
            cm.execute_query(connection, query)

update_all()
    