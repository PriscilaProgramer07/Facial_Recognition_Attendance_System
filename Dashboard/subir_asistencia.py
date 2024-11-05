import streamlit as st
import random
from datetime import datetime, timedelta
from database_operations import DynamoDBManager
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Crear una instancia de DynamoDBManager
db_manager = DynamoDBManager()

# Función para generar asistencia aleatoria
def generate_random_attendance():
    try:
        st.write("Iniciando generación de registros de asistencia...")
        start_date = datetime(2024, 10, 14)
        end_date = datetime.now()

        # Lista de estados de asistencia
        attendance_statuses = ["Present", "Absent", "Late"]

        # Obtener todos los cursos y estudiantes
        courses = db_manager.get_all_courses()
        students = db_manager.get_all_students()

        if not courses or not students:
            st.error("No se encontraron cursos o estudiantes en la base de datos.")
            return

        for course in courses:
            course_id = course['course_id']

            for student in students:
                matricula = student['matricula']

                # Asegurarse de que la matrícula sea numérica
                if isinstance(matricula, str):
                    matricula = int(matricula)

                # Generar asistencias desde el 14 de octubre hasta hoy
                current_date = start_date
                while current_date <= end_date:
                    # Generar estado de asistencia aleatorio
                    attendance_status = random.choice(attendance_statuses)
                    attendance_time = current_date.strftime("%H:%M:%S")

                    # Crear registro de asistencia
                    result = db_manager.insert_attendance(
                        matricula=matricula,
                        attendance_date=current_date.strftime("%Y-%m-%d"),
                        course_id=course_id,
                        attendance_time=attendance_time,
                        attendance_status=attendance_status
                    )

                    if "successfully" in result:
                        logging.info(f"Registro añadido exitosamente: {result}")
                    else:
                        logging.error(f"Error al añadir registro: {result}")

                    current_date += timedelta(days=1)

        st.success("Asistencia generada y añadida correctamente.")
    except Exception as e:
        logging.error(f"Error al generar registros de asistencia: {str(e)}")
        st.error(f"Error al generar registros de asistencia: {str(e)}")

# Llamada directa para generar asistencia
generate_random_attendance()
