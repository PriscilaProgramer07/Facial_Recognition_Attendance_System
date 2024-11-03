# AWS Commands

### Install aws-shell
```bash
pip install aws-shell
```

### Configure AWS CLI
```bash
aws configure
```

### Create a Collection on AWS Rekognition
```bash
aws rekognition create-collection --collection-id facerecognition_collection --region us-east-1
```

### Create a Table on DynamoDB
```bash
aws dynamodb create-table --table-name facerecognition \
--attribute-definitions AttributeName=RekognitionId,AttributeType=S \
--key-schema AttributeName=RekognitionId,KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
--region us-east-1
```

### Create an S3 Bucket
```bash
aws s3 mb s3://bucket-name --region us-east-1
```

