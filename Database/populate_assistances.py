import boto3
import random
from datetime import datetime, timedelta
import os

# Initialize DynamoDB client
dynamodb = boto3.client(
    'dynamodb',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
)

ATTENDANCE_TABLE_NAME = 'Attendance'

# List of attendance statuses with weights for random choice
attendance_statuses = ['Present'] * 75 + ['Absent'] * 15 + ['Late'] * 10

# Function to record attendance in DynamoDB
def record_attendance(matricula, course_id, attendance_date, attendance_status):
    try:
        attendance_time = datetime.now().strftime("%H:%M:%S")
        attendance_date_course_id = f"{matricula}_{attendance_date}_{course_id}"

        item = {
            'attendance_date_course_id': {'S': attendance_date_course_id},
            'matricula': {'N': str(matricula)},
            'course_id': {'S': course_id},
            'Date': {'S': attendance_date},
            'Time': {'S': attendance_time},
            'Status': {'S': attendance_status},
            'attendance_date': {'S': attendance_date},
            'attendance_time': {'S': attendance_time},
            'attendance_status': {'S': attendance_status}
        }

        dynamodb.put_item(
            TableName=ATTENDANCE_TABLE_NAME,
            Item=item
        )

        print(f"Attendance recorded for matricula {matricula} on {attendance_date} for course {course_id}. Status: {attendance_status}")
    except Exception as e:
        print(f"Error recording attendance for matricula {matricula} on {attendance_date}: {str(e)}")

# Function to populate attendance for a list of students and courses
def populate_attendance(matriculas, course_ids, start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        attendance_date_str = current_date.strftime("%Y-%m-%d")
        for course_id in course_ids:
            for matricula in matriculas:
                # Randomly choose an attendance status
                attendance_status = random.choice(attendance_statuses)
                # Record the attendance
                record_attendance(matricula, course_id, attendance_date_str, attendance_status)
        
        # Move to the next day
        current_date += timedelta(days=1)

# Example usage
if __name__ == "__main__":
    # List of matriculas
    matriculas = [
        2109012, 2009009, 2109021, 2009020, 2109028, 2109048, 2109050,
        2009048, 2109058, 2109061, 2109077, 2109099, 2109104, 2109128,
        2009121, 2109139, 2109145, 2109148
    ]

    # List of course IDs
    course_ids = ["TD2024", "VM2024", "OW2024", "E92024", "BI2024", "DE2024", "NLP2024"]

    # Date range for the test
    start_date = datetime(2024, 10, 14)  # Start date for the test
    end_date = datetime(2024, 11, 2)  # End date for the test

    # Populate the attendance records
    populate_attendance(matriculas, course_ids, start_date, end_date)