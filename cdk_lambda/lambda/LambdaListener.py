# @author Varun Singh
# @email admin@talkhash.com
# @create date 2021-06-19 15:45:54
# @modify date 2021-06-19 15:45:54
# @desc AWS CDK Lambda + S3 Event Stack


import boto3
import os
import json

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')


def handler(event, context):
    bucket_name = (os.environ['BUCKET_NAME'])
    key = event['Records'][0]['s3']['object']['key']
    size = event['Records'][0]['s3']['object']['size']
    image = {
        'S3Object': {
            'Bucket': bucket_name,
            'Name': key
        }
    }

    try:
        # Write results to DynamoDB
        dynamodb.put_item(TableName=(os.environ['TABLE_NAME']),
                          Item={
            'image_name': {'S': key}
        }
        )

        response = {'status': 'success', 'key': key}
        return response

    except Exception as e:
        print(e)
        print("[Error] :: Error processing object {} from bucket {}. ".format(
            key, bucket_name))
        raise e
