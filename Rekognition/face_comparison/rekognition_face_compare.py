import boto3
import io
from PIL import Image

# Initialize the clients without explicitly setting the region here.
# The region and credentials are picked up from environment variables.
rekognition = boto3.client('rekognition')
dynamodb = boto3.client('dynamodb')

image_path = input("Enter path of the image to check: ")

image = Image.open(image_path)
stream = io.BytesIO()
image.save(stream, format="JPEG")
image_binary = stream.getvalue()

response = rekognition.search_faces_by_image(
    CollectionId='facerecognition_collection',
    Image={'Bytes': image_binary}
)

found = False
for match in response['FaceMatches']:
    print(match['Face']['FaceId'], match['Face']['Confidence'])
    
    face = dynamodb.get_item(
        TableName='facerecognition',  
        Key={'RekognitionId': {'S': match['Face']['FaceId']}}
    )
    
    if 'Item' in face:
        print("Found Person: ", face['Item']['FullName']['S'])
        found = True

if not found:
    print("Person cannot be recognized")
