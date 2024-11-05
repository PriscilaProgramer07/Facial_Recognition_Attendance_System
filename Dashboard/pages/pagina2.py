import streamlit as st
import login
from database_operations import DynamoDBManager
import boto3
from botocore.exceptions import ClientError
import io
import string

# Generate the login session
login.generarLogin()

# Check if the user is authenticated
if 'usuario' in st.session_state:
    st.header('Register a :violet[New] Student')

    # Create an instance of DynamoDBManager
    db_manager = DynamoDBManager()

    # AWS S3 client setup
    s3 = boto3.client('s3')

    # Specify your S3 bucket name for storing student photos
    S3_BUCKET_NAME = 'upypersons-images'
    REKOGNITION_COLLECTION_ID = 'facerecognition_collection'

    # Available programs for selection (with accents)
    programs = [
        "Ingeniería en Ciberseguridad",
        "Ingeniería en Datos",
        "Ingeniería en Robótica Computacional",
        "Ingeniería en Sistemas Embebidos Computacionales"
    ]

    # Create a form for student registration
    def registration_form():
        with st.form("student_registration_form", clear_on_submit=True):
            student_id = st.text_input("Student ID")
            first_name = st.text_input("First Name")
            last_name_1 = st.text_input("Last Name (Paternal)")
            last_name_2 = st.text_input("Last Name (Maternal)")
            email = st.text_input("Email")
            grade = st.number_input("Grade", min_value=0, max_value=10, step=1)
            group = st.text_input("Group (A-Z)").upper()
            program = st.selectbox("Program", programs)

            # Only option to take a photo
            photo = st.camera_input("Take a photo")

            # Submit button for the form
            submit_button = st.form_submit_button("Register Student")

            return submit_button, student_id, first_name, last_name_1, last_name_2, email, grade, group, program, photo

    # Display the registration form and get form data
    submit_button, student_id, first_name, last_name_1, last_name_2, email, grade, group, program, photo = registration_form()

    # Process form submission
    if submit_button:
        # Validate that the group is a single letter from A-Z
        if not (len(group) == 1 and group in string.ascii_uppercase):
            st.error("Group must be a single letter from A to Z.")
        elif not photo:
            st.error("Please take a photo to continue.")
        else:
            try:
                # Store the image bytes in memory to avoid re-reading a closed file
                image_bytes = photo.read()

                # Upload the photo to S3 using the in-memory bytes
                s3.upload_fileobj(
                    io.BytesIO(image_bytes),
                    S3_BUCKET_NAME,
                    f"index/{student_id}.jpg",
                    ExtraArgs={'ContentType': 'image/jpeg', 'Metadata': {'FullName': student_id}}
                )

                # Register the face in Rekognition using the same in-memory bytes
                rekognition = boto3.client('rekognition')
                response = rekognition.index_faces(
                    CollectionId=REKOGNITION_COLLECTION_ID,
                    Image={'Bytes': image_bytes},
                    ExternalImageId=student_id,
                    DetectionAttributes=['ALL']
                )

                if response['FaceRecords']:
                    # Insert student details into DynamoDB
                    result = db_manager.insert_student(
                        matricula=student_id,
                        nombre=first_name,
                        apellido1=last_name_1,
                        apellido2=last_name_2,
                        correo=email,
                        grado=str(grade),  # Convert to string to match DynamoDB types
                        grupo=group,
                        carrera=program
                    )
                    st.success(f"Student {first_name} registered successfully with photo.")
                else:
                    st.error("Face registration failed. Please try again with a clear photo.")

            except ClientError as e:
                st.error(f"An error occurred: {e.response['Error']['Message']}")
