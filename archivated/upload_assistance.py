#Code to upload an assistance to the assitance collection

import os
import datetime
import pymongo
from pymongo import MongoClient

# Get the MongoDB connection string from the environment variable
MONGODB_URI = os.getenv('MONGODB_URI')
if not MONGODB_URI:
    raise ValueError("Please set the MONGODB_URI environment variable.")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)

# Define the database and collection (replace with your actual database and collection names)
db = client['attendance_system']  # Replace with your database name
attendance_collection = db['attendance']  # Replace with your collection name
students_collection = db['students']  # Replace with your Students collection name
teachers_collection = db['teachers']  # Replace with your Teachers collection name
courses_collection = db['courses']  # Replace with your Courses collection name





def insert_attendance_record(matricula: int, course_id: str, attendance_status: str = "Present"):
    """
    Inserts an attendance record into the MongoDB database.

    Parameters:
        matricula (int): The student's matricula (ID).
        course_id (str): The ID of the course.
        attendance_status (str): Status of the attendance, default is "Present".
    
    Returns:
        str: Message indicating success or failure.
    """
    # Define the attendance date and time
    attendance_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    attendance_time = datetime.datetime.now()

    # Create a unique attendance_id using matricula, attendance_date, and course_id
    attendance_id = f"{matricula}_{attendance_date.date()}_{course_id}"

    # Create the attendance document
    attendance_record = {
        "attendance_id": attendance_id,
        "matricula": matricula,
        "course_id": course_id,
        "attendance_date": attendance_date,
        "attendance_time": attendance_time,
        "attendance_status": attendance_status
    }

    try:
        # Insert the attendance record into the collection
        result = attendance_collection.insert_one(attendance_record)
        return f"Attendance record inserted with _id: {result.inserted_id}"
    except pymongo.errors.DuplicateKeyError:
        return "Duplicate attendance record. This attendance has already been logged."
    except Exception as e:
        return f"An error occurred: {str(e)}"



def insert_student(matricula: int, nombre: str, apellido1: str, apellido2: str, correo: str, grado: int, grupo: str, carrera: str):
    """
    Inserts a student record into the MongoDB database.

    Parameters:
        matricula (int): Student's unique ID.
        nombre (str): Student's first name.
        apellido1 (str): Student's first last name.
        apellido2 (str): Student's second last name.
        correo (str): Student's email.
        grado (int): Student's grade.
        grupo (str): Student's group or section.
        carrera (str): Student's major or program.
    
    Returns:
        str: Message indicating success or failure.
    """
    student_record = {
        "matricula": matricula,
        "nombre": nombre,
        "apellido1": apellido1,
        "apellido2": apellido2,
        "correo": correo,
        "grado": grado,
        "grupo": grupo,
        "carrera": carrera
    }

    try:
        result = students_collection.insert_one(student_record)
        return f"Student record inserted with _id: {result.inserted_id}"
    except pymongo.errors.DuplicateKeyError:
        return "Duplicate student record. A student with this matricula already exists."
    except Exception as e:
        return f"An error occurred: {str(e)}"


def insert_teacher(teacher_id: str, nombre: str, apellido1: str, apellido2: str, correo: str, password: str, courses_managed: list):
    """
    Inserts a teacher record into the MongoDB database.

    Parameters:
        teacher_id (str): Teacher's unique ID.
        nombre (str): Teacher's first name.
        apellido1 (str): Teacher's first last name.
        apellido2 (str): Teacher's second last name.
        correo (str): Teacher's email.
        password (str): Hashed password for the teacher.
        courses_managed (list): List of course IDs that the teacher manages.
    
    Returns:
        str: Message indicating success or failure.
    """
    teacher_record = {
        "teacher_id": teacher_id,
        "nombre": nombre,
        "apellido1": apellido1,
        "apellido2": apellido2,
        "correo": correo,
        "password": password,
        "courses_managed": courses_managed
    }

    try:
        result = teachers_collection.insert_one(teacher_record)
        return f"Teacher record inserted with _id: {result.inserted_id}"
    except pymongo.errors.DuplicateKeyError:
        return "Duplicate teacher record. A teacher with this ID already exists."
    except Exception as e:
        return f"An error occurred: {str(e)}"




def insert_course(course_id: str, course_name: str, students_enrolled: list, teacher_id: str):
    """
    Inserts a course record into the MongoDB database.

    Parameters:
        course_id (str): Unique identifier for the course.
        course_name (str): Name of the course.
        students_enrolled (list): List of student matriculas enrolled in the course.
        teacher_id (str): ID of the teacher responsible for the course.
    
    Returns:
        str: Message indicating success or failure.
    """
    course_record = {
        "course_id": course_id,
        "course_name": course_name,
        "students_enrolled": students_enrolled,
        "teacher_id": teacher_id
    }

    try:
        result = courses_collection.insert_one(course_record)
        return f"Course record inserted with _id: {result.inserted_id}"
    except pymongo.errors.DuplicateKeyError:
        return "Duplicate course record. A course with this ID already exists."
    except Exception as e:
        return f"An error occurred: {str(e)}"






# Close the MongoDB connection when done (in a real application, ensure you close connections properly)
def close_connection():
    client.close()
    print("MongoDB connection closed.")

def main():

    # Call the function to insert attendance for the student 2009048 in course DE2024
    response = insert_attendance_record(matricula=2009048, course_id="DE2024")

    # Print the response to see the result
    print(response)


    # Insert a new student
    student_response = insert_student(
        matricula=222222,
        nombre="John",
        apellido1="Doe",
        apellido2="Smith",
        correo="222222@upy.edu.mx",
        grado=9,
        grupo="B",
        carrera="Ingeniería en Datos"
    )
    print(student_response)

    # Insert a new teacher
    teacher_response = insert_teacher(
        teacher_id="TCH1015",
        nombre="Jane",
        apellido1="Smith",
        apellido2="Johnson",
        correo="jane.smith@upy.edu.mx",
        password="hashed_password",  # Make sure this is properly hashed
        courses_managed=["VM2024", "TD2024"]
    )
    print(teacher_response)

    # Insert a new course
    course_response = insert_course(
        course_id="skb2024",
        course_name="SKIBIDI 2024",
        students_enrolled=[2009048, 222222],  # Add student matriculas enrolled in the course
        teacher_id="TCH1015"
    )
    print(course_response)    


    # Close the MongoDB connection after the operation
    close_connection()


main()