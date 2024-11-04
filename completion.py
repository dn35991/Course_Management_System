import courses_module as cm
import personal as p

# This program will allow you to change the completion status of a course

connection = cm.database_connection(p.HOST_NAME, p.USERNAME, p.PASSWORD, cm.DATABASE)

course_code = input("What is the course code of the course?: ")
cm.print_list(cm.COMPLETION_TYPES)
status = int(input("What is the new completion status of the course?: "))

def completion_query():
    query = f"""
    UPDATE
    course_info
    SET 
        Completion = "{cm.COMPLETION_TYPES[status - 1]}"
    WHERE
        CourseCode = "{course_code}";
    """
    cm.execute_query(connection, query)
    return

def term_query(term):
    query = f"""
    UPDATE
    course_info
    SET 
        Term = {term}
    WHERE
        CourseCode = "{course_code}";
    """
    cm.execute_query(connection, query)
    return

def grade_query(grade):
    query = f"""
    UPDATE
    course_info
    SET 
        Grade = {grade}
    WHERE
        CourseCode = "{course_code}";
    """
    cm.execute_query(connection, query)
    return

def change_completion():
    if status == 1:
        term = input("What term was this course completed?: ")
        grade = input("What is the achieved grade of this course?: ")
        completion_query()
        term_query(f"\"{term}\"")
        grade_query(grade)
    elif status == 2 or status == 3:
        term = input("What term is this course in?: ")
        completion_query()
        term_query(f"\"{term}\"")
        grade_query("NULL")
    elif status == 4:
        completion_query()
        term_query("NULL")
        grade_query("NULL")
    elif status == 5:
        completion_query()
        term_query("NULL")
        grade_query("NULL")
    else:
        return        

change_completion()
