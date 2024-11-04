import courses_module as cm
import personal as p

# This program will allow you to add a single course and all of its information including the prerequisites
#   into both tables
 
connection = cm.database_connection(p.HOST_NAME, p.USERNAME, p.PASSWORD, cm.DATABASE)

course_code = input("What is the course code (ABCD 000)?: ")
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

def add_course():
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

def add_prereqs():
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
    
add_course()
add_prereqs()