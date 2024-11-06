# Face Attendance Recognition System

  

## Overview

The **Face Attendance Recognition System** is an end-to-end solution that automates attendance logging using facial recognition technology. This project includes a fully integrated user interface, data storage, and cloud-based machine learning for facial recognition. It is designed to streamline attendance tracking for educational institutions or organizations.

  

## Features

-  **User Authentication**: Secure login system using hashed passwords.

-  **Face Recognition**: Captures and identifies faces using AWS Rekognition.

-  **Attendance Logging**: Records attendance in AWS DynamoDB with unique composite keys.

-  **Real-Time Dashboard**: Built with Streamlit for easy access and management of attendance data.

-  **Attendance Reports**: Generate and download detailed reports of attendance records.

-  **Data Management**: Functions to insert, retrieve, and update student, teacher, and course data in DynamoDB.

  

Click for access: https://priscilaprogramer07-facial-recognition-a-dashboardinicio-agrhui.streamlit.app/

  
  
  

## Technologies Used

-  **Streamlit**: For creating an interactive web-based dashboard.

-  **Pandas**: For handling and processing data from CSV files.

-  **Boto3**: To interact with AWS services like Rekognition and DynamoDB.

-  **AWS Rekognition**: Facial recognition service for identifying students.

-  **AWS DynamoDB**: NoSQL database for storing data related to students, teachers, courses, and attendance records.

-  **AWS S3**: Optional, for storing images.

-  **bcrypt**: For hashing passwords to secure user credentials.

-  **Python Standard Libraries**:

	-  `os`: For handling environment variables and file paths.

	-  `io`: For managing image data.

	-  `datetime`: For date and time handling.

  

## Project Structure

Facial_Recognition_Attendance_System/

│

├── Dashboard/

│ ├── dashboard.py # Main Streamlit app

│ ├── login.py # Authentication and session management

│ ├── usuarios.csv # User data CSV (now pulled from GitHub)

│ └── utils.py # Utility functions for handling DynamoDB operations

│

├── Database/

│ ├── jsons/

│ │ ├── courses.json # Sample data for courses

│ │ └── students.json # Sample data for students

│ ├── populate_data.py # Script for populating DynamoDB tables

│

├── Pages/

│ ├── inicio.py # Page for viewing the student list

│ ├── pagina1.py # Attendance page

│ ├── pagina2.py # New student registration page

│ ├── pagina3.py # Attendance report page

│ └── pagina4.py # About page

│

└── requirements.txt # Python package dependencies

  

## Setup Instructions

  

### Prerequisites

-  **Python >= 3.8+**

-  **AWS Account** with IAM roles configured for Rekognition and DynamoDB access.

-  **Git** to clone the repository.

  

### Step-by-Step Guide

1.  **Clone the repository**:

```bash

git clone https://github.com/your-repo/Facial_Recognition_Attendance_System.git

cd Facial_Recognition_Attendance_System
```
  

2.  **Set up a virtual environment (recommended):**
```bash
python -m venv .venv

source .venv/bin/activate # On Windows use .venv\Scripts\activate
```
  

3.  **Install dependencies**
```bash
pip install -r requirements.txt
```
  

4.  **Set up AWS credentials:**

Ensure your AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_DEFAULT_REGION are set as environment variables. You can add them to your ~/.bashrc, ~/.zshrc, or use a .env file.

  

5.  **Run the Streamlit app:**
```bash
streamlit run Dashboard/dashboard.py
```
  
  

### Usage

  

1. Login: Enter your credentials to access the dashboard.

2. Attendance Marking: Use the camera input to capture an image and mark attendance.

3. Attendance Reports: View and download attendance summaries for specific date ranges.

4. New Student Registration: Add new student details to the system.

5. Logout: Use the logout button to end your session.

  

### Sample Data

  

Use the provided JSON files in Database/jsons/ to populate your database for testing:

  

- courses.json: Contains sample course data.

- students.json: Contains sample student data.

  

### Security Considerations

  

- Ensure that sensitive data, such as AWS credentials, are stored securely and not exposed in your code.

- Use bcrypt for password hashing to enhance the security of user authentication.

  

### Future Improvements

  

- Implement real-time facial recognition for continuous attendance tracking.

- Add more detailed analytics for attendance trends.

- Integrate additional user roles and permissions.

  

### Author

  

Developed by

- **Data Engineers**: Priscila Tzuc, Julio Dzul

- **Data Scientists**: Antonio Ruiz, Luis Martinez

- **Data Analysts**: Angel Campos, Angel Sansores

  
  

# AWS Commands

  

### Install aws-shell

```bash

pip  install  aws-shell

```

  

### Configure AWS CLI

```bash

aws  configure

```

  

### Create a Collection on AWS Rekognition

```bash

aws  rekognition  create-collection  --collection-id  facerecognition_collection  --region  us-east-1

```

  

### Create a Table on DynamoDB

```bash

aws  dynamodb  create-table  --table-name  facerecognition  \

--attribute-definitions  AttributeName=RekognitionId,AttributeType=S  \

--key-schema  AttributeName=RekognitionId,KeyType=HASH  \

--provisioned-throughput  ReadCapacityUnits=1,WriteCapacityUnits=1  \

--region  us-east-1

```

  

### Create an S3 Bucket

```bash

aws  s3  mb  s3://bucket-name  --region  us-east-1

```
