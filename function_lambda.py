from __future__ import print_function
 
import boto3
import json
import urllib
 
print('Loading function')
 
# Initialize clients for DynamoDB, S3, and Rekognition
dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
 
# --------------- Helper Functions ------------------
 
def index_faces(bucket, key):
    # Index faces in the specified Rekognition collection
    response = rekognition.index_faces(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": key
            }
        },
        CollectionId="facerecognition_collection"  # Ensure this collection is created beforehand
    )
    return response
 
def update_index(tableName, faceId, fullName):
    # Update DynamoDB table with RekognitionId and FullName
    response = dynamodb.put_item(
        TableName=tableName,
        Item={
            'RekognitionId': {'S': faceId},
            'FullName': {'S': fullName}
        }
    )
    return response
 
# --------------- Main handler ------------------
 
def lambda_handler(event, context):
    # Print the event data to understand its structure (useful for debugging)
    print("Received event:", json.dumps(event, indent=2))
 
    # Get the bucket and object key from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print("Processing file:", key)
 
    try:
        # Step 1: Call Rekognition to index faces in the image
        response = index_faces(bucket, key)
        print("Rekognition response:", json.dumps(response, indent=2))
 
        # Step 2: If indexing was successful, get the faceId and metadata
        if response['ResponseMetadata']['HTTPStatusCode'] == 200 and 'FaceRecords' in response and len(response['FaceRecords']) > 0:
            faceId = response['FaceRecords'][0]['Face']['FaceId']
            print("Detected FaceId:", faceId)
 
            # Step 3: Retrieve the 'fullname' metadata from the S3 object
            ret = s3.head_object(Bucket=bucket, Key=key)
            personFullName = ret['Metadata'].get('fullname', 'Unknown')  # Default to 'Unknown' if metadata is missing
            print("FullName from Metadata:", personFullName)
 
            # Step 4: Update DynamoDB with faceId and full name
            update_index('facerecognition', faceId, personFullName)
            print("Successfully updated DynamoDB with FaceId and FullName.")
 
        else:
            print("Rekognition did not detect any faces or there was an issue with the response.")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Successfully processed image and updated DynamoDB')
        }
 
    except Exception as e:
        print("Error processing file {} from bucket {}: {}".format(key, bucket, str(e)))
        raise e