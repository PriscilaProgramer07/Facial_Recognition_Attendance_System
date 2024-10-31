import streamlit as st
from database_operations import DynamoDBManager  # Assuming this is where your class is located

# Initialize DynamoDBManager
db_manager = DynamoDBManager()

# Streamlit UI
st.title("DynamoDB Students Table")

# Section to insert a test student
st.header("Insert Test Student")
if st.button("Test Insert"):
    result = db_manager.insert_student(
        matricula=111111,
        nombre="Hageo",
        apellido1="Cruz",
        apellido2="Ramayo",
        correo="111111@upy.edu.mx",
        grado=9,
        grupo="A",
        carrera="Ingeniería en Datos"
    )
    st.write(result)

# Section to display all students
st.header("View All Students")
if st.button("Show Students Table"):
    students = db_manager.get_all_students()
    if students:
        st.write("Students in the database:")
        st.write(students)  # Display raw data for simplicity
    else:
        st.write("No students found or error retrieving data.")