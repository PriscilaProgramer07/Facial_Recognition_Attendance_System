import streamlit as st
import login
from database_operations import DynamoDBManager
import pandas as pd

# Generate the login session
login.generarLogin()

# Check if the user is authenticated
if 'usuario' in st.session_state:
    st.header('List of :violet[Students] ')

    # Create an instance of DynamoDBManager
    db_manager = DynamoDBManager()

    # Get the list of all students
    try:
        students = db_manager.get_all_students()

        if students:
            # Create a DataFrame to organize and display the data
            student_data = [
                {
                    'Matricula': int(str(student['matricula']).replace(",", "")),  # Convert to integer for proper sorting
                    'Name': f"{student['nombre']} {student['apellido1']} {student['apellido2']}",
                    'Program': student['carrera'],
                    'Grade/Group': f"{student['grado']}{student['grupo']}",
                    'Grade': student['grado'],
                    'Group': student['grupo']
                }
                for student in students
            ]

            # Convert to DataFrame
            df_students = pd.DataFrame(student_data)

            # Define full range of options for filters
            all_programs = [
                "Ingeniería en Ciberseguridad",
                "Ingeniería en Datos",
                "Ingeniería en Robótica Computacional",
                "Ingeniería en Sistemas Embebidos Computacionales"
            ]
            all_grades = list(range(0, 11))  # Grades from 0 to 10
            all_groups = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')  # Groups A-Z

            # Get unique values for filters that exist in the data
            programs = sorted(set(all_programs) | set(df_students['Program'].unique()))
            grades = sorted(set(all_grades) | set(df_students['Grade'].unique()))
            groups = sorted(set(all_groups) | set(df_students['Group'].unique()))

            # User selects filters
            selected_program = st.selectbox("Select Program", options=programs)
            selected_grade = st.selectbox("Select Grade", options=grades)
            selected_group = st.selectbox("Select Group", options=groups)

            # Filter DataFrame based on user selection
            filtered_df = df_students[
                (df_students['Program'] == selected_program) &
                (df_students['Grade'] == selected_grade) &
                (df_students['Group'] == selected_group)
            ]

            # Convert 'Matricula' back to string to remove commas and sort
            filtered_df['Matricula'] = filtered_df['Matricula'].astype(str)
            filtered_df = filtered_df.sort_values(by='Matricula')

            # Drop extra columns for display
            filtered_df = filtered_df[['Matricula', 'Name', 'Program', 'Grade/Group']]

            # Display the filtered DataFrame
            if not filtered_df.empty:
                st.subheader(f'List of Registered Students for {selected_program} {selected_grade}{selected_group}')
                st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)
            else:
                st.warning(f"No students found for {selected_program} {selected_grade}{selected_group}.")

        else:
            st.write("No students found in the database.")
            # Display full range of filter options even if no students exist
            st.selectbox("Select Program", options=[
                "Ingeniería en Ciberseguridad",
                "Ingeniería en Datos",
                "Ingeniería en Robótica Computacional",
                "Ingeniería en Sistemas Embebidos Computacionales"
            ])
            st.selectbox("Select Grade", options=list(range(0, 11)))
            st.selectbox("Select Group", options=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

    except Exception as e:
        st.error(f"An error occurred while retrieving students: {str(e)}")
else:
    st.warning("Please log in to view the student list.")
