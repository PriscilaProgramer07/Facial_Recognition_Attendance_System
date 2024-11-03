import os
import pymongo
import boto

# MongoDB connection
MONGODB_URI = os.getenv('MONGODB_URI')
client = pymongo.MongoClient(MONGODB_URI)
db = client['your_database_name']

# AWS DynamoDB connection
dynamodb = boto3.resource('dynamodb', region_name='your_region')  # Replace 'your_region' with your AWS region

# Define the DynamoDB tables
students_table = dynamodb.Table('Students')
courses_table = dynamodb.Table('Courses')
attendance_table = dynamodb.Table('Attendance')
teachers_table = dynamodb.Table('Teachers')

# Migrate students
def migrate_students():
    students = db['Students'].find()
    for student in students:
        students_table.put_item(
            Item={
                'matricula': student['matricula'],
                'nombre': student['nombre'],
                'apellido1': student['apellido1'],
                'apellido2': student['apellido2'],
                'correo': student['correo'],
                'grado': student['grado'],
                'grupo': student['grupo'],
                'carrera': student['carrera']
            }
        )
    print("Student data migration completed.")

# Migrate courses
def migrate_courses():
    courses = db['Courses'].find()
    for course in courses:
        courses_table.put_item(
            Item={
                'course_id': course['course_id'],
                'course_name': course['course_name'],
                'teacher_id': course['teacher_id'],
                'students_enrolled': course['students_enrolled']
            }
        )
    print("Course data migration completed.")

# Migrate attendance
def migrate_attendance():
    attendances = db['Attendance'].find()
    for attendance in attendances:
        attendance_table.put_item(
            Item={
                'matricula': attendance['matricula'],
                'attendance_date_course_id': f"{attendance['attendance_date']}_{attendance['course_id']}",
                'attendance_date': str(attendance['attendance_date']),
                'course_id': attendance['course_id'],
                'attendance_time': str(attendance['attendance_time']),
                'attendance_status': attendance['attendance_status']
            }
        )
    print("Attendance data migration completed.")

# Migrate teachers
def migrate_teachers():
    teachers = db['Teachers'].find()
    for teacher in teachers:
        teachers_table.put_item(
            Item={
                'teacher_id': teacher['teacher_id'],
                'nombre': teacher['nombre'],
                'correo': teacher['correo'],
                'password': teacher['password'],
                'courses_managed': teacher['courses_managed']
            }
        )
    print("Teacher data migration completed.")

# Run migration functions
migrate_students()
migrate_courses()
migrate_attendance()
migrate_teachers()

# Close MongoDB connection
client.close()
