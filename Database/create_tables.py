import boto3

# Initialize a DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Change the region if needed

def create_students_table():
    table = dynamodb.create_table(
        TableName='Students',
        KeySchema=[
            {'AttributeName': 'matricula', 'KeyType': 'HASH'}  # Partition Key
        ],
        AttributeDefinitions=[
            {'AttributeName': 'matricula', 'AttributeType': 'N'}  # 'N' stands for Number
        ],
        BillingMode='PAY_PER_REQUEST'  # Use on-demand capacity mode
    )
    return table

def create_teachers_table():
    table = dynamodb.create_table(
        TableName='Teachers',
        KeySchema=[
            {'AttributeName': 'teacher_id', 'KeyType': 'HASH'}  # Partition Key
        ],
        AttributeDefinitions=[
            {'AttributeName': 'teacher_id', 'AttributeType': 'S'}  # 'S' stands for String
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    return table

def create_courses_table():
    table = dynamodb.create_table(
        TableName='Courses',
        KeySchema=[
            {'AttributeName': 'course_id', 'KeyType': 'HASH'}  # Partition Key
        ],
        AttributeDefinitions=[
            {'AttributeName': 'course_id', 'AttributeType': 'S'}
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    return table

def create_attendance_table():
    table = dynamodb.create_table(
        TableName='Attendance',
        KeySchema=[
            {'AttributeName': 'matricula', 'KeyType': 'HASH'},  # Partition Key
            {'AttributeName': 'attendance_date_course_id', 'KeyType': 'RANGE'}  # Sort Key
        ],
        AttributeDefinitions=[
            {'AttributeName': 'matricula', 'AttributeType': 'N'},
            {'AttributeName': 'attendance_date_course_id', 'AttributeType': 'S'}
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    return table

# Create all tables
def main():
    print("Creating tables...")
    students_table = create_students_table()
    teachers_table = create_teachers_table()
    courses_table = create_courses_table()
    attendance_table = create_attendance_table()

    # Wait until all tables are created
    students_table.meta.client.get_waiter('table_exists').wait(TableName='Students')
    teachers_table.meta.client.get_waiter('table_exists').wait(TableName='Teachers')
    courses_table.meta.client.get_waiter('table_exists').wait(TableName='Courses')
    attendance_table.meta.client.get_waiter('table_exists').wait(TableName='Attendance')

    print("All tables created successfully!")

if __name__ == "__main__":
    main()