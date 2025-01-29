import courses_module as cm
import personal as p

# This program will allow you to add the academic plan of a single course to the academic plan table.
#   Be sure to write each input as specificied in the question prompts.

connection = cm.database_connection(p.HOST_NAME, p.USERNAME, p.PASSWORD, p.DATABASE)

requirement_options = [
    "Mandatory",
    "Required Choice",
    "Not Required"]

cm.PLAN_COLUMNS.remove("CourseCode")

course_code = input("What is the course code: ")

def plan_query(code, column, option):
    query = f"""
    UPDATE academic_plan
    SET `{column}` = "{option}"
    WHERE CourseCode = "{code}";
    """
    return query
    
def add_plan(code):
    for column in cm.PLAN_COLUMNS:
        cm.print_list(requirement_options)
        option = int(input(f"What is the requirement for \"{column}\"?: "))
        if 0 < option <= len(requirement_options):
            cm.execute_query(connection, plan_query(code, column, requirement_options[option - 1]))
        else:
            continue
    return

add_plan(course_code)
