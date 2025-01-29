import courses_module as cm
import personal as p


# This program will allow you to add a single course and all of its information including the prerequisites
#   and academic plan into all tables
 
connection = cm.database_connection(p.HOST_NAME, p.USERNAME, p.PASSWORD, p.DATABASE)

requirement_options = [
    "Mandatory",
    "Required Choice",
    "Not Required"
]

cm.PLAN_COLUMNS.remove("CourseCode")

code = input("What is the course code (ABCD 000)?: ")
course_name = input("What is the name of the course?: ")
credits = input("How many credits is the course worth?: ")
cm.print_list(cm.COURSE_TYPE)
course_type = int(input("What type of course is it?: "))
cm.print_list(cm.COMPLETION_TYPES)
completion = int(input("What is the completion status of the course?: "))

def add_query(course_code, course_name, credits, course_type, completion, term, grade):
    query = f"""
    INSERT INTO
        course_info
    VALUES
        ("{course_code}", "{course_name}", {credits}, "{cm.COURSE_TYPE[course_type - 1]}", "{cm.COMPLETION_TYPES[completion - 1]}", {term}, {grade})
    """
    cm.execute_query(connection, query)
    return

def add_new_plan(course_code):
    query = f"""
    INSERT INTO
        academic_plan (CourseCode)
    VALUES
        ("{course_code}")
    """
    cm.execute_query(connection, query)
    return

def add_course(course_code):
    if completion == 4 or completion == 5:
        add_query(course_code, course_name, credits, course_type, completion, "NULL", "NULL")
        print(f"{cm.COMPLETION_TYPES[completion - 1]} Course Added")
    elif completion == 3 or completion == 2:
        term = input("What term is/will the course be completed? ")
        add_query(course_code, course_name, credits, course_type, completion, f"\"{term}\"", "NULL")
        print(f"{cm.COMPLETION_TYPES[completion - 1]} Course Added")
    elif completion == 1:
        term = input("What term is/will the course be completed? ")
        grade = input("What grade has been acheived for the course?: ")
        add_query(completion, course_name, credits, course_type, completion, f"\"{term}\"", grade)
        print(f"{cm.COMPLETION_TYPES[completion - 1]} Course Added")
    else:
        print("No course was added")
        return

def add_prereqs(course_code):
    n = 0
    while True:
        pcode = input("What is the prerequisite course code?: ")
        minimum = input("What is the minimum grade required?: ")

        if pcode == "":
            print(f"{n} Prerequistes Added for {course_code}")
            return
        elif minimum == "":
            query = f"""
            INSERT INTO
                prerequisite_courses
            VALUES
                ("{course_code}", "{pcode}", NULL);
            """
            cm.execute_query(connection, query)
            pcode = ""
            n = n + 1 
        else:
            query = f"""
            INSERT INTO
                prerequisite_courses
            VALUES
                ("{course_code}", "{pcode}", {minimum});
            """
            cm.execute_query(connection, query)
            pcode = ""
            minimum = ""
            n = n + 1 

    print(f"{n} Prerequistes Added for {course_code}")

def plan_query(course_code, column, option):
    query = f"""
    UPDATE academic_plan
    SET `{column}` = \"{option}\"
    WHERE CourseCode = \"{course_code}\";
    """
    return query
    
def add_plan(course_code):
    for column in cm.PLAN_COLUMNS:
        cm.print_list(requirement_options)
        option = int(input(f"What is the requirement for \"{column}\"? "))
        if 0 < option <= len(requirement_options):
            cm.execute_query(connection, plan_query(course_code, column, requirement_options[option - 1]))
        else:
            continue
    return

add_course(code)
add_new_plan(code)
add_prereqs(code)
add_plan(code)