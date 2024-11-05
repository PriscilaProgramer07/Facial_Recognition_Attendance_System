import boto3 
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import logging

# Configura el logger
logging.basicConfig(level=logging.INFO)

class DynamoDBManager:
    def __init__(self, region_name='us-east-1'):
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.dynamodb_client = boto3.client('dynamodb', region_name=region_name)
        self.students_table = self.dynamodb.Table('Students')
        self.teachers_table = self.dynamodb.Table('Teachers')
        self.courses_table = self.dynamodb.Table('Courses')
        self.attendance_table = self.dynamodb.Table('Attendance')

    def insert_student(self, matricula, nombre, apellido1, apellido2, correo, grado, grupo, carrera):
        """Insert a student into the Students table if it doesn't already exist."""
        try:
            self.students_table.put_item(
                Item={
                    'matricula': str(matricula),  # Almacenar como cadena para asegurar compatibilidad
                    'nombre': nombre,
                    'apellido1': apellido1,
                    'apellido2': apellido2,
                    'correo': correo,
                    'grado': str(grado),
                    'grupo': grupo,
                    'carrera': carrera
                },
                ConditionExpression='attribute_not_exists(matricula)'  # Ensures no overwrite
            )
            return f"Student with matricula {matricula} inserted successfully."
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                return f"Student with matricula {matricula} already exists and cannot be inserted."
            logging.error(f"Error inserting student: {e.response['Error']['Message']}")
            return f"Error inserting student: {e.response['Error']['Message']}"

    def get_all_students(self):
        """Fetch all students from the Students table."""
        try:
            response = self.students_table.scan()
            return response.get('Items', [])
        except ClientError as e:
            logging.error(f"Error fetching students: {e.response['Error']['Message']}")
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
                    'courses_managed': courses_managed  # List of course IDs as String Set
                }
            )
            return f"Teacher with ID {teacher_id} inserted successfully."
        except ClientError as e:
            logging.error(f"Error inserting teacher: {e.response['Error']['Message']}")
            return f"Error inserting teacher: {e.response['Error']['Message']}"

    def insert_course(self, course_id, course_name, students_enrolled, teacher_id):
        """Insert a course into the Courses table."""
        try:
            self.courses_table.put_item(
                Item={
                    'course_id': course_id,
                    'course_name': course_name,
                    'students_enrolled': [str(student) for student in students_enrolled],  # List of student matriculas as strings
                    'teacher_id': teacher_id
                }
            )
            return f"Course with ID {course_id} inserted successfully."
        except ClientError as e:
            logging.error(f"Error inserting course: {e.response['Error']['Message']}")
            return f"Error inserting course: {e.response['Error']['Message']}"

    def insert_attendance(self, matricula, attendance_date, course_id, attendance_time, attendance_status):
        """Insert an attendance record into the Attendance table."""
        try:
            if not matricula or not attendance_date or not course_id:
                logging.error("Uno o más campos requeridos están vacíos (matricula, attendance_date, course_id).")
                return "Error: One or more required fields are missing (matricula, attendance_date, course_id)."

            attendance_date_course_id = f"{matricula}_{attendance_date}_{course_id}"

            # Verificar todos los valores de entrada
            logging.info("Valores generados para la inserción:")
            logging.info(f"Matricula: {matricula}")
            logging.info(f"Attendance Date: {attendance_date}")
            logging.info(f"Course ID: {course_id}")
            logging.info(f"Generated attendance_date_course_id: {attendance_date_course_id}")
            logging.info(f"Attendance Time: {attendance_time}")
            logging.info(f"Attendance Status: {attendance_status}")

            item = {
                'attendance_date_course_id': attendance_date_course_id,
                'matricula': str(matricula),  # Confirmar formato como cadena
                'attendance_date': attendance_date,
                'attendance_time': attendance_time,
                'attendance_status': attendance_status,
                'course_id': course_id
            }

            # Imprimir el Item antes de la inserción
            logging.info("Item a insertar:")
            logging.info(item)

            self.attendance_table.put_item(Item=item)
            return f"Attendance record for student {matricula} on {attendance_date} for course {course_id} inserted successfully."
        except ClientError as e:
            logging.error(f"Error al insertar el registro de asistencia: {e.response['Error']['Message']}")
            return f"Error inserting attendance record: {e.response['Error']['Message']}"
        except ValueError:
            logging.error("Error: Matricula must be a valid integer.")
            return "Error: Matricula must be a valid integer."
        except Exception as e:
            logging.error(f"Error inesperado: {str(e)}")
            return f"Unexpected error: {str(e)}"

    def get_attendance_records(self, course_id, start_date, end_date):
        """Retrieve attendance records for a specific course and date range."""
        try:
            start_date_str = start_date.strftime("%Y-%m-%d")
            end_date_str = end_date.strftime("%Y-%m-%d")

            # Realizar un escaneo con filtro por course_id y rango de fechas
            response = self.attendance_table.scan(
                FilterExpression=Attr('course_id').eq(course_id) & Attr('attendance_date').between(start_date_str, end_date_str)
            )

            attendances = response.get('Items', [])

            # Formatear los registros de asistencia
            formatted_records = []
            for record in attendances:
                formatted_record = {
                    'Matricula': record.get('matricula', ''),
                    'Date': record.get('attendance_date', ''),
                    'Time': record.get('attendance_time', ''),
                    'Status': record.get('attendance_status', ''),
                    'Course ID': record.get('course_id', '')
                }
                formatted_records.append(formatted_record)

            return formatted_records
        except Exception as e:
            logging.error(f"Error retrieving attendance records: {str(e)}")
            return []

    def get_all_courses(self):
        """Fetch all courses from the Courses table."""
        try:
            response = self.courses_table.scan()
            return response.get('Items', [])
        except Exception as e:
            logging.error(f"Error al obtener cursos: {str(e)}")
            return []

    def get_student_by_face_id(self, face_id):
        """Retrieve a student by face ID from the Students table."""
        try:
            response = self.students_table.scan(
                FilterExpression=Attr("face_id").eq(face_id)
            )
            items = response.get('Items', [])
            if items:
                return items[0]  # Devuelve el primer resultado que coincida
            else:
                return None
        except Exception as e:
            logging.error(f"Error al obtener estudiante por face ID: {str(e)}")
            return None
