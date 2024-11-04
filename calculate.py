import courses_module as cm
import personal as p

# This program will allow you to calcualte different types of values depending on different variables

connection = cm.database_connection(p.HOST_NAME, p.USERNAME, p.PASSWORD, cm.DATABASE)

calculation_options = [
    "Average Grade",
    "Math Average",
    "Number of Course Type",
    "Total Credits"
]

cm.print_list(calculation_options)
type = int(input("WHat would you like to calculate?: "))

def calculate_avg():
    query = """
    SELECT 
        ROUND(AVG(Grade), 2)
    FROM
        course_info
    WHERE 
        Completion = "Completed" AND
        Grade IS NOT NULL;
    """
    return query

def math_avg():
    query = """
    SELECT 
        ROUND(AVG(Grade), 2)
    FROM
        course_info
    WHERE 
        Completion = "Completed" AND
        Grade IS NOT NULL AND
        CourseType = "Math";
    """
    return query

def num_course_type():
    cm.print_list(cm.COMPLETION_TYPES + ["All"])
    completion = int(input("What completion status would you like to calculate?: "))
    if 1 <= completion <= 5:
        query = f"""
        SELECT
            COUNT(CourseCode)
        FROM 
            course_info
        WHERE 
            Completion = "{cm.COMPLETION_TYPES[completion - 1]}";
        """
    elif completion == 6:
        query = """
        SELECT
            COUNT(CourseCode)
        FROM 
            course_info;
        """
    else:
        return
    return query

def num_credit():
    cm.print_list(["Course Type", "Completion Type", "All Completed Coures (Excluding PD Courses)"])
    column = int(input("How you like to view the number of credits?: "))
    if column == 1:
        cm.print_list(cm.COURSE_TYPE)
        type = int(input("What type of course would you like to view?: "))
        query = f"""
        SELECT
            SUM(Credits)
        FROM 
            course_info
        WHERE 
            CourseType = "{cm.COURSE_TYPE[type - 1]}" AND
            Completion = "Completed";
        """
    elif column == 2:
        cm.print_list(cm.COMPLETION_TYPES)
        status = int(input("What course status would you like to view (excludes PD courses)?: "))
        query = f"""
        SELECT
            SUM(Credits)
        FROM 
            course_info
        WHERE 
            Completion = "{cm.COMPLETION_TYPES[status - 1]}" AND
            CourseType != "PD";
        """
    elif column == 3:
        query = """
        SELECT
            SUM(Credits)
        FROM 
            course_info
        WHERE 
            Completion = "Completed" AND
            CourseType != "PD";
        """
    else:
        return
    return query

table = []

def calculate():
    if type == 1:
        query = calculate_avg()
        cm.display_info(connection, query, ["Cumulative Average"], table)
    elif type == 2:
        query = math_avg()
        cm.display_info(connection, query, ["Math Average"], table)
    elif type == 3:
        query = num_course_type()
        cm.display_info(connection, query, ["Number of Courses"], table)
    elif type == 4:
        query = num_credit()
        cm.display_info(connection, query, ["Number of Credits"], table)
    else:
        return
    
calculate()
    