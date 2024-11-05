import streamlit as st
import pandas as pd
from datetime import datetime
from database_operations import DynamoDBManager
import login

# Generar la sesión de inicio de sesión
login.generarLogin()

# Verificar si el usuario está autenticado
if 'usuario' in st.session_state:
    st.header(':violet[Attendance Report] Generator')

    # Crear una instancia de DynamoDBManager
    db_manager = DynamoDBManager()

    # Obtener la lista de todos los cursos
    try:
        courses = db_manager.get_all_courses()
        if courses:
            # Convertir los cursos a un diccionario para la selección
            course_options = {course['course_name']: course['course_id'] for course in courses}

            # Seleccionar curso
            selected_course_name = st.selectbox("Select Course", options=list(course_options.keys()))
            selected_course_id = course_options[selected_course_name]

            # Obtener todos los estudiantes para filtrar por grado y grupo
            students = db_manager.get_all_students()
            if students:
                # Crear un DataFrame con los estudiantes
                student_df = pd.DataFrame(students)

                # Obtener los valores únicos de grado y grupo
                unique_grades = student_df['grado'].unique()
                unique_groups = student_df['grupo'].unique()

                # Selectores de grado y grupo
                selected_grade = st.selectbox("Select Grade", options=sorted(unique_grades))
                selected_group = st.selectbox("Select Group", options=sorted(unique_groups))

                # Filtrar los estudiantes por grado y grupo
                filtered_students = student_df[
                    (student_df['grado'] == selected_grade) & (student_df['grupo'] == selected_group)
                ]

                # Seleccionar el rango de fechas
                start_date = st.date_input("Select Start Date", value=datetime(2024, 11, 1))
                end_date = st.date_input("Select End Date", value=datetime(2024, 11, 30))

                if st.button("Generate Report"):
                    # Obtener registros de asistencia para el curso y rango de fechas seleccionados
                    attendance_records = db_manager.get_attendance_records(selected_course_id, start_date, end_date)

                    if attendance_records:
                        # Formatear el DataFrame de asistencia
                        attendance_df = pd.DataFrame(attendance_records)

                        # Fusionar los datos de asistencia con los datos de estudiantes filtrados
                        merged_df = pd.merge(
                            filtered_students,
                            attendance_df,
                            how='left',
                            left_on='matricula',
                            right_on='Matricula'
                        )

                        # Ordenar por apellidos y mostrar los datos relevantes
                        merged_df['FullName'] = merged_df['apellido1'] + ' ' + merged_df['apellido2'] + ' ' + merged_df['nombre']
                        merged_df.sort_values(by=['apellido1', 'apellido2', 'nombre'], inplace=True)

                        # Seleccionar las columnas de fechas y la asistencia
                        date_columns = pd.to_datetime(attendance_df['Date']).dt.strftime('%Y-%m-%d').unique()
                        pivot_df = merged_df.pivot_table(
                            index=['matricula', 'FullName'],
                            columns='Date',
                            values='Status',
                            aggfunc='first',
                            fill_value='Absent'
                        )

                        # Restablecer el índice para que la matrícula y el nombre sean columnas visibles
                        pivot_df.reset_index(inplace=True)

                        # Convertir la columna 'matricula' a una cadena sin formato de miles
                        pivot_df['matricula'] = pivot_df['matricula'].apply(lambda x: str(x).replace(',', ''))

                        # Ordenar por 'FullName' (apellido)
                        pivot_df.sort_values(by='FullName', inplace=True)

                        # Mostrar la tabla en la app de Streamlit
                        st.dataframe(pivot_df)

                        # Descargar el CSV
                        csv = pivot_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name=f"{selected_course_name}_attendance_report_{start_date}_{end_date}.csv",
                            mime='text/csv',
                        )
                    else:
                        st.warning(f"No attendance records found for {selected_course_name} between {start_date} and {end_date}.")
            else:
                st.error("No students found in the database.")
        else:
            st.error("No courses found in the database.")
    except Exception as e:
        st.error(f"Error processing course data: {str(e)}")
else:
    st.warning("Please log in to access the attendance report generator.")
