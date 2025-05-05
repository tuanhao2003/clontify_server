import boto3
from django.conf import settings
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)

class UploadService:
    def __init__(self):
        self.s3Client = boto3.client(
            's3',
            aws_access_key_id=getattr(settings, "AWS_ACCESS_KEY_ID",""),
            aws_secret_access_key=getattr(settings, "AWS_SECRET_ACCESS_KEY",""),
            region_name=getattr(settings, "AWS_S3_REGION_NAME","")
        )
        self.bucket_name = getattr(settings, "AWS_STORAGE_BUCKET_NAME","")
    
    def upload_file(self, file_obj, key, content_type=None):
        extra_args = {}
        if content_type:
            extra_args['ContentType'] = content_type
            
        try:
            self.s3Client.upload_fileobj(
                file_obj,
                self.bucket_name,
                key,
                ExtraArgs=extra_args
            )
            return f"https://{getattr(settings, "AWS_S3_CUSTOM_DOMAIN","")}/{key}"
        except ClientError as e:
            logger.error(f"Error uploading file to S3: {e}")
            return None
    
    def generate_presigned_url(self, key, expiration=3600):
        try:
            url = self.s3Client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': key
                },
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            logger.error(f"Error generating presigned URL: {e}")
            return None