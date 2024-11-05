import streamlit as st
import boto3
import io
from PIL import Image
import os

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

# Function to process the image with Rekognition
def recognize_face(image_bytes):
    try:
        # Call Rekognition to search for faces in the provided image
        response = rekognition.search_faces_by_image(
            CollectionId=REKOGNITION_COLLECTION_ID,
            Image={'Bytes': image_bytes}
        )
        
        # Check for face matches
        for match in response['FaceMatches']:
            face_id = match['Face']['FaceId']
            confidence = match['Face']['Confidence']

            # Fetch the corresponding person details from DynamoDB
            face_data = dynamodb.get_item(
                TableName=DYNAMODB_TABLE_NAME,
                Key={'RekognitionId': {'S': face_id}}
            )

            # Check if an item was found
            if 'Item' in face_data:
                full_name = face_data['Item']['FullName']['S']
                return full_name, confidence

        # No match found
        return None, None

    except Exception as e:
        st.error(f"An error occurred during recognition: {str(e)}")
        return None, None

def main():
    st.title("Face Attendance System")
    st.write("Capture your image for attendance marking.")

    # Camera input to capture an image
    image = st.camera_input("Take a photo")

    # Select the course (pre-defined for demonstration)
    course_id = st.selectbox("Select the course", ["NLP2024", "DE2024", "BI2024"])

    if image:
        # Convert the image to bytes for sending to Rekognition
        image_bytes = image.read()

        # Call the function to recognize the face
        full_name, confidence = recognize_face(image_bytes)

        # Display the result
        if full_name:
            st.success(f"Recognized Person: {full_name} with {confidence:.2f}% confidence.")
            # Here you can call your function to upload the attendance if necessary
            # Example: upload_attendance(recognized_matricula, course_id)
        else:
            st.error("Person cannot be recognized. Please try again.")

if __name__ == "__main__":
    main()
