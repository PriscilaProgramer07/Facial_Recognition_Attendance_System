import json
import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Adjust region as needed

# Define paths to your JSON files
courses_json_path = '/Users/pulie/Documents/facial_recognition_tests/Database/jsons/courses.json'
students_json_path = '/Users/pulie/Documents/facial_recognition_tests/Database/jsons/students.json'

# Define DynamoDB table names
courses_table_name = 'Courses'
students_table_name = 'Students'

def load_json_data(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def insert_courses(data):
    """Insert data into the Courses table."""
    table = dynamodb.Table(courses_table_name)
    for item in data:
        table.put_item(Item=item)
    print(f"Inserted {len(data)} items into {courses_table_name} table.")

def insert_students(data):
    """Insert data into the Students table."""
    table = dynamodb.Table(students_table_name)
    for item in data:
        table.put_item(Item=item)
    print(f"Inserted {len(data)} items into {students_table_name} table.")

def main():
    # Load data from JSON files
    courses_data = load_json_data(courses_json_path)
    students_data = load_json_data(students_json_path)
    
    # Insert data into DynamoDB tables
    insert_courses(courses_data)
    insert_students(students_data)

if __name__ == "__main__":
    main()