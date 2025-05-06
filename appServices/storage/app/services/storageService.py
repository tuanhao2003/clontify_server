import boto3
import os
from botocore.exceptions import ClientError
from django.conf import settings
from app.models import File
from common.errorCodes import ErrorCodes
import uuid

class StorageService:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def upload_file(self, file, file_type):
        try:
            # Generate unique file name
            file_extension = os.path.splitext(file.name)[1]
            file_name = f"{uuid.uuid4()}{file_extension}"
            
            # Upload to S3
            self.s3_client.upload_fileobj(
                file,
                self.bucket_name,
                file_name,
                ExtraArgs={
                    'ContentType': file.content_type,
                    'ACL': 'public-read'
                }
            )

            # Generate S3 URL
            s3_url = f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{file_name}"

            # Save file metadata to database
            file_record = File(
                fileName=file.name,
                fileType=file_type,
                fileSize=file.size,
                s3Key=file_name,
                s3Bucket=self.bucket_name,
                s3Url=s3_url
            )
            file_record.save()

            return file_record, None
        except ClientError as e:
            return None, ErrorCodes.OPERATION_FAILED
        except Exception as e:
            return None, ErrorCodes.OPERATION_FAILED

    def delete_file(self, file_id):
        try:
            file_record = File.objects.get(id=file_id)
            
            # Delete from S3
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_record.s3Key
            )

            # Delete from database
            file_record.delete()
            return True, None
        except File.DoesNotExist:
            return None, ErrorCodes.NOT_FOUND
        except ClientError as e:
            return None, ErrorCodes.OPERATION_FAILED
        except Exception as e:
            return None, ErrorCodes.OPERATION_FAILED

    def get_file(self, file_id):
        try:
            file_record = File.objects.get(id=file_id)
            return file_record, None
        except File.DoesNotExist:
            return None, ErrorCodes.NOT_FOUND
        except Exception as e:
            return None, ErrorCodes.OPERATION_FAILED

    def get_presigned_url(self, file_id, expiration=3600):
        try:
            file_record = File.objects.get(id=file_id)
            
            # Generate presigned URL
            presigned_url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': file_record.s3Key
                },
                ExpiresIn=expiration
            )
            
            return presigned_url, None
        except File.DoesNotExist:
            return None, ErrorCodes.NOT_FOUND
        except ClientError as e:
            return None, ErrorCodes.OPERATION_FAILED
        except Exception as e:
            return None, ErrorCodes.OPERATION_FAILED 