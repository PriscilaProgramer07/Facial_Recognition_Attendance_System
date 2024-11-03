import boto3
from botocore.exceptions import ClientError

class DynamoDBManager:
    def __init__(self, region_name='us-east-1'):
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.students_table = self.dynamodb.Table('Students')
        self.teachers_table = self.dynamodb.Table('Teachers')
        self.courses_table = self.dynamodb.Table('Courses')
        self.attendance_table = self.dynamodb.Table('Attendance')

    def insert_student(self, matricula, nombre, apellido1, apellido2, correo, grado, grupo, carrera):
        """Insert a student into the Students table."""
        try:
            self.students_table.put_item(
                Item={
                    'matricula': matricula,
                    'nombre': nombre,
                    'apellido1': apellido1,
                    'apellido2': apellido2,
                    'correo': correo,
                    'grado': grado,
                    'grupo': grupo,
                    'carrera': carrera
                }
            )
            return f"Student with matricula {matricula} inserted successfully."
        except ClientError as e:
            return f"Error inserting student: {e.response['Error']['Message']}"

    def get_all_students(self):
        """Fetch all students from the Students table."""
        try:
            response = self.students_table.scan()
            return response.get('Items', [])
        except ClientError as e:
            return f"Error fetching students: {e.response['Error']['Message']}"

    def insert_teacher(self, teacher_id, nombre, apellido1, apellido2, correo, password, courses_managed):
        """Insert a teacher into the Teachers table."""
        try:
            self.teachers_table.put_item(
                Item={
                    'teacher_id': teacher_id,
                    'nombre': nombre,
                    'apellido1': apellido1,
                    'apellido2': apellido2,
                    'correo': correo,
                    'password': password,  # Assume password is hashed already
                    'courses_managed': courses_managed  # List of course IDs
                }
            )
            return f"Teacher with ID {teacher_id} inserted successfully."
        except ClientError as e:
            return f"Error inserting teacher: {e.response['Error']['Message']}"

    def insert_course(self, course_id, course_name, students_enrolled, teacher_id):
        """Insert a course into the Courses table."""
        try:
            self.courses_table.put_item(
                Item={
                    'course_id': course_id,
                    'course_name': course_name,
                    'students_enrolled': students_enrolled,  # List of student matriculas
                    'teacher_id': teacher_id
                }
            )
            return f"Course with ID {course_id} inserted successfully."
        except ClientError as e:
            return f"Error inserting course: {e.response['Error']['Message']}"

    def insert_attendance(self, matricula, attendance_date, course_id, attendance_time, attendance_status):
        """Insert an attendance record into the Attendance table."""
        attendance_date_course_id = f"{attendance_date}_{course_id}"  # Composite key
        try:
            self.attendance_table.put_item(
                Item={
                    'matricula': matricula,
                    'attendance_date_course_id': attendance_date_course_id,
                    'attendance_date': attendance_date,
                    'attendance_time': attendance_time,
                    'attendance_status': attendance_status
                }
            )
            return f"Attendance record for student {matricula} on {attendance_date} for course {course_id} inserted successfully."
        except ClientError as e:
            return f"Error inserting attendance record: {e.response['Error']['Message']}"