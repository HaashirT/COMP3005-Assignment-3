import psycopg2
from psycopg2 import sql

# Database connection settings
DB_CONFIG = {
    'dbname': 'COMP3005_A3',
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': '5432'
}

# Connect to the PostgreSQL database
def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print("Error connecting to database:", e)
        return None
    
# Retrieve and display all students from table
def getAllStudents() -> None:
    conn = get_connection()
    if not conn: # Stop if failed connection
        return
    
    try: 
        with conn.cursor() as cursor: 
            sql = "SELECT * FROM students ORDER BY student_id;"
            cursor.execute(sql)
            students = cursor.fetchall() # Get all rows from query's result
            print("\nAll Students:")

            # Loop through each student and print details
            for s in students:
                print(f"ID: {s[0]}, Name: {s[1]} {s[2]}, Email: {s[3]}, Enrolled: {s[4]}")
    
    except Exception as e:
        print("Erorr retrieving students:", e)
    
    finally:
        conn.close() # Close connection

# Add a new student to the table given a first name, last name, email, and enrollment date
def addStudent(first_name: str, last_name: str, email: str, enrollment_date: str) -> None:
    conn = get_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO students (first_name, last_name, email, enrollment_date)
            VALUES (%s, %s, %s, %s)
            RETURNING student_id;
            """
            cursor.execute(sql, (first_name, last_name, email, enrollment_date))
            student_id = cursor.fetchone()[0]
            conn.commit()
            print(f"Student added with ID: {student_id}")
    
    except Exception as e:
        print("Error adding student:", e)
        conn.rollback()

    finally:
        conn.close()

# Update a student's email address by their ID
def updateStudentEmail(student_id: int, new_email: str) -> None:
    conn = get_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE students SET email = %s WHERE student_id = %s;"
            cursor.execute(sql, (new_email, student_id))

            if cursor.rowcount == 0:
                print("No student found with that ID.")

            else:
                conn.commit()
                print(f"Student ID {student_id} email updated to {new_email}.")

    except Exception as e:
        print("Error updating email:", e)
        conn.rollback()

    finally:
        conn.close()

# Delete a student record by their ID
def deleteStudent(student_id: int) -> None:
    conn = get_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM students WHERE student_id = %s;"
            cursor.execute(sql, (student_id,))

            if cursor.rowcount == 0:
                print("No student found with that ID.")

            else:
                conn.commit()
                print(f"Student ID {student_id} deleted successfully.")

    except Exception as e:
        print("Error deleting student:", e)
        conn.rollback()

    finally:
        conn.close()

# Prompt the user to select an option using a text-based user interface
def main() -> None:
    get_connection()
    
    while True:
        print("\nSelect Option:\n[0] Exit\n[1] Get all students\n[2] Add student\n[3] Update student email\n[4] Delete student")

        user_input = input("\nEnter choice: ")
        
        if user_input == "0":
            print("\nExiting...")
            return

        elif user_input == "1":
            getAllStudents()
        
        elif user_input == "2":
            first_name = input("\nEnter student's first name: ")
            last_name = input("\nEnter student's last name: ")
            email = input("\nEnter student's email: ")
            enrollment_date = input("\nEnter student's enrollment date: ")

            addStudent(first_name, last_name, email, enrollment_date)
        
        elif user_input == "3":
            student_id = input("\nEnter student id: ")
            new_email = input("\nEnter new email: ")

            updateStudentEmail(student_id, new_email)
        
        elif user_input == "4":
            student_id = input("\nEnter student id: ")
            deleteStudent(student_id)
        
        else:
            print("\nInvalid selection.")
            
main()