import streamlit as st
import pymongo
import bcrypt
import os
from pymongo import MongoClient

# MongoDB connection setup
MONGODB_URI = os.getenv('MONGODB_URI')
if not MONGODB_URI:
    st.error("Please set the MONGODB_URI environment variable.")
    st.stop()

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client['your_database_name']  # Replace with your database name
teachers_collection = db['Teachers']  # Replace with your Teachers collection name

# Function to hash the password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

# Function to verify password
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Function to register a teacher
def register_teacher(teacher_id, nombre, apellido1, apellido2, correo, password, courses_managed):
    hashed_password = hash_password(password)
    
    teacher_record = {
        "teacher_id": teacher_id,
        "nombre": nombre,
        "apellido1": apellido1,
        "apellido2": apellido2,
        "correo": correo,
        "password": hashed_password.decode('utf-8'),  # Store as a string for readability
        "courses_managed": courses_managed
    }

    try:
        teachers_collection.insert_one(teacher_record)
        return "Teacher registered successfully!"
    except pymongo.errors.DuplicateKeyError:
        return "A teacher with this ID or email already exists."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to login a teacher
def login_teacher(correo, password):
    # Retrieve the teacher's record from the database
    teacher = teachers_collection.find_one({"correo": correo})
    if teacher and verify_password(password, teacher['password']):
        return teacher
    else:
        return None

# Streamlit UI for registration and login
def main():
    st.title("Teacher Dashboard")

    # Check if the user is already logged in
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['teacher'] = None

    # Show login or registration options based on login state
    if not st.session_state['logged_in']:
        option = st.selectbox("Choose an option", ["Login", "Register"])

        if option == "Login":
            st.header("Login")
            correo = st.text_input("Email")
            password = st.text_input("Password", type='password')

            if st.button("Login"):
                teacher = login_teacher(correo, password)
                if teacher:
                    st.session_state['logged_in'] = True
                    st.session_state['teacher'] = teacher
                    st.success(f"Welcome, {teacher['nombre']}!")
                else:
                    st.error("Invalid email or password. Please try again.")

        elif option == "Register":
            st.header("Teacher Registration")
            teacher_id = st.text_input("Teacher ID", max_chars=20)
            nombre = st.text_input("First Name")
            apellido1 = st.text_input("Last Name (First)")
            apellido2 = st.text_input("Last Name (Second)")
            correo = st.text_input("Email")
            password = st.text_input("Password", type='password')
            courses_managed = st.multiselect(
                "Courses Managed",
                options=["NLP2024", "DE2024", "BI2024", "VM2024"],  # Replace with actual course IDs
                help="Select the courses that the teacher will manage."
            )

            if st.button("Register"):
                if not teacher_id or not nombre or not apellido1 or not correo or not password or not courses_managed:
                    st.error("Please fill out all fields.")
                else:
                    result = register_teacher(teacher_id, nombre, apellido1, apellido2, correo, password, courses_managed)
                    st.success(result) if "successfully" in result else st.error(result)
    else:
        st.header(f"Welcome, {st.session_state['teacher']['nombre']}")
        st.write("You are logged in.")

        # Add any post-login functionalities here, like managing courses or viewing attendance
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['teacher'] = None
            st.success("Logged out successfully")

# Run the Streamlit app
if __name__ == "__main__":
    main()
