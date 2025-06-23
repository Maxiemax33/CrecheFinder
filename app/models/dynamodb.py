import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# DynamoDB client setup
dynamodb = boto3.resource(
    'dynamodb',
    region_name='ap-south-1',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

users_table = dynamodb.Table("Users")
creches_table = dynamodb.Table("Creches")
reviews_table = dynamodb.Table("Reviews")
