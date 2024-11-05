import streamlit as st
from database_operations import DynamoDBManager  # Assuming this is where your class is located

# Initialize DynamoDBManager
db_manager = DynamoDBManager()

st.title("DynamoDB Attendance Records")

# Section to display attendance records
st.header("View Attendance Records for a Group")
grade = st.number_input("Grade", min_value=1, max_value=12)
group = st.text_input("Group")
career = st.text_input("Career")  # Input for career
course_id = st.text_input("Course ID")  # New input for course ID
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

if st.button("Retrieve Attendance"):
    result = db_manager.get_attendances_for_group(grade, group, career, course_id, str(start_date), str(end_date))
    if isinstance(result, list) and result:
        st.write(f"Attendance records for grade {grade}, group {group}, career {career}, and course {course_id}:")
        st.write(result)
    else:
        st.write(result)