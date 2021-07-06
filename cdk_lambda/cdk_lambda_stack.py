# @author Varun Singh
# @email admin@talkhash.com
# @create date 2021-07-06 15:45:54
# @modify date 2021-07-06 15:45:54
# @desc AWS CDK Lambda + S3 Event Stack


from aws_cdk import (
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_s3_notifications as s3_notifications,
    core as cdk
)


class CdkLambdaStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create new IAM group and use
        group = iam.Group(self, "VSGroup")
        user = iam.User(self, "VSUser")

        # Add IAM user to the group
        user.add_to_group(group)

        # Create S3 Bucket
        bucket = s3.Bucket(self, 'vs-bucket')
        bucket.grant_read_write(user)

        # Create a lambda function
        lambda_func = _lambda.Function(
            self, 'LambdaListener',
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler='LambdaListener.handler',
            code=_lambda.Code.asset('cdk_lambda\lambda'),
            environment={
                'BUCKET_NAME': bucket.bucket_name
            })

        # Create trigger for Lambda function with image type suffixes
        notification = s3_notifications.LambdaDestination(lambda_func)
        notification.bind(self, bucket)
        bucket.add_object_created_notification(
            notification, s3.NotificationKeyFilter(suffix='.jpg'))
        bucket.add_object_created_notification(
            notification, s3.NotificationKeyFilter(suffix='.jpeg'))
        bucket.add_object_created_notification(
            notification, s3.NotificationKeyFilter(suffix='.png'))
