import streamlit as st
import login
import boto3
import os
from datetime import datetime
from PIL import Image

# Ensure AWS environment variables are set
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")  # Default to 'us-east-1'

# Validate AWS credentials
if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION]):
    st.error("AWS credentials are not set. Please set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_DEFAULT_REGION.")
    st.stop()

# Initialize boto3 clients using environment variables
rekognition = boto3.client(
    'rekognition',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION
)

dynamodb = boto3.client(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION
)

# Define the AWS Rekognition Collection ID and DynamoDB Table
REKOGNITION_COLLECTION_ID = 'facerecognition_collection'
DYNAMODB_TABLE_NAME = 'facerecognition'  # Replace with your table name
COURSES_TABLE_NAME = 'Courses'  # Replace with your courses table name
ATTENDANCE_TABLE_NAME = 'Attendance'  # Replace with your attendance table name

# Function to get all courses from DynamoDB
def get_all_courses():
    try:
        response = dynamodb.scan(TableName=COURSES_TABLE_NAME)
        courses = response.get('Items', [])
        course_dict = {course['course_name']['S']: course['course_id']['S'] for course in courses}
        return course_dict
    except Exception as e:
        st.error(f"Error fetching courses: {str(e)}")
        return {}

# Function to process the image with Rekognition
def recognize_face(image_bytes):
    try:
        response = rekognition.search_faces_by_image(
            CollectionId=REKOGNITION_COLLECTION_ID,
            Image={'Bytes': image_bytes}
        )
        
        for match in response['FaceMatches']:
            face_id = match['Face']['FaceId']
            confidence = match['Face']['Confidence']

            face_data = dynamodb.get_item(
                TableName=DYNAMODB_TABLE_NAME,
                Key={'RekognitionId': {'S': face_id}}
            )

            if 'Item' in face_data:
                full_name = face_data['Item'].get('FullName', {}).get('S', 'Unknown')
                matricula = int(full_name)  # Convert to integer if necessary
                return full_name, matricula, confidence

        return None, None, None

    except Exception as e:
        st.error(f"An error occurred during recognition: {str(e)}")
        return None, None, None

# Function to check if attendance is already recorded
def is_attendance_already_recorded(matricula, course_id, attendance_date):
    try:
        response = dynamodb.query(
            TableName=ATTENDANCE_TABLE_NAME,
            KeyConditionExpression="matricula = :mat AND begins_with(attendance_date_course_id, :prefix)",
            ExpressionAttributeValues={
                ":mat": {'N': str(matricula)},
                ":prefix": {'S': f"{matricula}_{attendance_date}_{course_id}"}
            }
        )
        return 'Items' in response and len(response['Items']) > 0  # True si existe, False si no
    except Exception as e:
        st.error(f"Error checking existing attendance: {str(e)}")
        return False

# Function to record attendance in DynamoDB
def record_attendance(matricula, course_id):
    try:
        attendance_date = datetime.today().strftime("%Y-%m-%d")
        attendance_time = datetime.now().strftime("%H:%M:%S")

        # Verificar si la asistencia ya fue registrada
        if is_attendance_already_recorded(matricula, course_id, attendance_date):
            return f"Attendance already recorded for student {matricula} on {attendance_date} for course {course_id}."

        attendance_date_course_id = f"{matricula}_{attendance_date}_{course_id}"

        item = {
            'attendance_date_course_id': {'S': attendance_date_course_id},
            'matricula': {'N': str(matricula)},  # Asegurar que matricula sea un número
            'course_id': {'S': course_id},
            'Date': {'S': attendance_date},
            'Time': {'S': attendance_time},
            'Status': {'S': 'Present'},
            'attendance_date': {'S': attendance_date},  # Agregar campo
            'attendance_time': {'S': attendance_time},  # Agregar campo
            'attendance_status': {'S': 'Present'}  # Agregar campo
        }

        # Insertar el item en DynamoDB
        dynamodb.put_item(
            TableName=ATTENDANCE_TABLE_NAME,
            Item=item
        )

        return "Attendance recorded successfully"
    except Exception as e:
        return f"Error recording attendance: {str(e)}"

# Main function to run the Streamlit app
def main():
    if 'usuario' in st.session_state:
        login.generarMenu(st.session_state['usuario'])
        
        st.title("Face :violet[Attendance] System")
        st.write("Capture your image for attendance marking.")

        # Restablecer variables de sesión para el formulario
        if 'image_uploaded' not in st.session_state:
            st.session_state['image_uploaded'] = None
        if 'confirmation_message' not in st.session_state:
            st.session_state['confirmation_message'] = ""

        courses = get_all_courses()
        if courses:
            course_name = st.selectbox("Select Course", options=list(courses.keys()), help="Choose the course for attendance")
            course_id = courses[course_name]

            image = st.camera_input("Take a photo", key='image_input')

            if image:
                st.session_state['image_uploaded'] = image.read()
                full_name, matricula, confidence = recognize_face(st.session_state['image_uploaded'])

                if full_name and matricula:
                    st.success(f"Recognized Person: {full_name} (Matricula: {matricula}) with {confidence:.2f}% confidence.")
                    
                    if st.button("Confirm Attendance"):
                        result = record_attendance(matricula, course_id)
                        if "successfully" in result:
                            st.session_state['confirmation_message'] = result
                            st.session_state['image_uploaded'] = None  # Restablecer la imagen cargada
                            st.write('<script>window.location.reload();</script>', unsafe_allow_html=True)  # Recargar la página
                        else:
                            st.error(result)
                else:
                    st.error("Person cannot be recognized. Please try again.")

            # Mostrar el mensaje de confirmación si está presente
            if st.session_state['confirmation_message']:
                st.success(st.session_state['confirmation_message'])
                st.session_state['confirmation_message'] = ""  # Limpiar el mensaje después de mostrarlo

        else:
            st.error("No courses available. Please check the database.")
    else:
        login.generarLogin()



if __name__ == "__main__":
    main()
